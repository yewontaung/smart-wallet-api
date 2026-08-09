from app.dtos.base import BaseDto


class ManagerAuthResult(BaseDto):

    access_token:str
    access_type:str = "Bearer"