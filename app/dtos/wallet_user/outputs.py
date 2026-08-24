from datetime import datetime
from typing import Literal, Optional

from app.dtos.base import BaseDto
from app.dtos.shared.outputs import UserRole


class SignInResult(BaseDto):
    verification_token:str
    expire_at:Optional[datetime] = None
    message:Optional[str] = None

class WalletUserAuthResult(BaseDto):
    access_token:str
    access_type:str = "Bearer"
    remember_token:str

    account_id:int
    phone:str
    full_name:str
    role:UserRole

class WalletBalance(BaseDto):
    wallet_id:int
    account_id:int
    current_balance:float
    phone_no:str