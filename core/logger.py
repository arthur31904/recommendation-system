import logging.handlers
import json
from .config import settings
from pydantic import BaseModel
from fastapi.responses import JSONResponse


class LogLevel:
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    FATAL = logging.FATAL


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "logger"
    LOG_FORMAT: str = '%(asctime)s.%(msecs)03d %(levelname)s  [%(servicename)s][%(handle)s][%(obj)s]%(message)s'
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = not settings.DEBUG
    # disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "logger": {"handlers": ["default"], "level": LOG_LEVEL},
    }


logger = logging.getLogger("logger")


class Logger:

    __logger = logger
    __server_name = 'settings.SERVER_NAME'

    @classmethod
    def log(cls, level, handle, payload, response, message):
        if isinstance(response, JSONResponse):
            response = json.loads(response.body)
        cls.__logger.log(level, msg=message,
                         extra={
                             "servicename": cls.__server_name,
                             "handle": handle,
                             "obj": cls.__form_obj(payload, response)
                         })

    @staticmethod
    def __form_obj(payload, response):
        log_user = "system"
        payload = [] if payload is None else [payload]
        response = [] if response is None else [response]

        return {
            "user_id": log_user,
            "input": payload,
            "output": response
        }
