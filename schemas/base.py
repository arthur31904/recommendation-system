from datetime import datetime
from typing import List, Union, Optional
from pydantic import BaseModel, AnyHttpUrl, validator

class create_base(BaseModel):

    name: Optional[Union[AnyHttpUrl, str]]
    url: Optional[Union[AnyHttpUrl, str]]

class edit_base(BaseModel):
    id: Optional[Union[AnyHttpUrl, str]]


class search_base(BaseModel):
    limit: Optional[Union[AnyHttpUrl, str]]
    page: Optional[Union[AnyHttpUrl, str]]




