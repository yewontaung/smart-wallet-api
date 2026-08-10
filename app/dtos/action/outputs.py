from app.dtos.base import BaseDto


class ActionResult(BaseDto):
    action_type:str
    message:str
