from typing import Any

from app.dtos.base import BaseDto


class ActionResult(BaseDto):
    action_result:Any
    action_type:str
    message:str
