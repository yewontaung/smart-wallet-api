from datetime import datetime
from typing import Optional

from app.dtos.base import BaseDto


class SignInResult(BaseDto):
    verification_token:str
    expire_at:Optional[datetime] = None
    message:Optional[str] = None

class WalletUserAuthResult(BaseDto):
    access_token:str
    access_type:str = "Bearer"