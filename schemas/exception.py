from pydantic import BaseModel
from typing import Optional, Any
class BizException(Exception):
    def __init__(self,
                 message: Any,
                 status_code: int = None):
        self.status_code = status_code
        self.message = message