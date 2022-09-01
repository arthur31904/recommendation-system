import secrets
from typing import List, Union
import os
from pydantic import AnyHttpUrl, BaseSettings, validator
from fastapi import Request

class Settings(BaseSettings):

    DEBUG: bool = os.getenv("DEBUG", False)
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str ='recommendation-system'
    # SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str='recommendation-system'

    ES_CONNECTION_URL: str='recommendation-system'

    @validator("ES_CONNECTION_URL", pre=True)
    def es_connection_url(cls, v: str) -> str:
        if len(v) > 0:
            return v
        else:
            raise ValueError(v)

    ES_INDEX: str = 'recommendation-system'

    @validator("ES_INDEX", pre=True)
    def es_index(cls, v: str) -> str:
        if len(v) > 0:
            return v
        else:
            raise ValueError(v)

    # PO_AWS_S3_URL: AnyHttpUrl ='https://fastapi.tiangolo.com/tutorial/sql-databases/#migrations'
    # S3_BUCKET_NAME: str ='recommendation-system'
    poredis: str = os.getenv('poredis')

    class Config:
        env_file = ".env"
        case_sensitive = True

def get_db(request: Request):
    return request.state.db

settings = Settings()
