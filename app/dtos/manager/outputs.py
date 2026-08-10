from datetime import datetime
from typing import Optional

from app.data.enums import ManagerRole, WalletUserType
from app.dtos.base import BaseDto


class ManagerAuthResult(BaseDto):

    access_token:str
    access_type:str = "Bearer"

class AccountListItem(BaseDto):
    user_id:int
    full_name:int
    nick_name:Optional[str] = None
    profile_url:Optional[str] = None
    account_type:WalletUserType
    phone_no:str
    created_at:datetime
    approved_at:datetime
    approver_id:int
    approver_full_name:str
    current_balance:float
    last_balance:float

class ManagerListItem(BaseDto):
    user_id:int
    full_name:int
    nick_name:Optional[str] = None
    profile_url:Optional[str] = None
    role:ManagerRole
    is_disable:bool
    phone_no:str
    created_at:datetime

class SupportChatListItem(BaseDto):
    chat_id:int
    created_at:int
    user_id:int
    full_name:int
    phone_no:int
    district_id:int
    district:str
    township_id:int
    township:str

    last_message_id:int
    last_message:str
    is_last_message_read:bool
    