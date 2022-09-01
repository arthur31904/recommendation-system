from pydantic import BaseModel
from typing import Optional, Any


class SuccessResponse(BaseModel):
    success = True
    message: Optional[Any] = None


class ErrorResponse(BaseModel):
    success = False
    message: Optional[Any] = None
