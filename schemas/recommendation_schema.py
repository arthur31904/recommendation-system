from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class sourceschema(BaseModel):
    """

    """
    pass

class Tag(sourceschema):
    """
    """
    tag_id: str


class TagIdList(BaseModel):
    """

    """
    tag_id_list: List[str]


class recommendation_back(sourceschema):
    """
    """
    movie_id: str


class recommendation_back_list(BaseModel):
    """

    """
    movie_ids: List[recommendation_back]


