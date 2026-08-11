from datetime import datetime
from typing import Optional

from app.data.enums import BusinessApprovalStatus, BusinessType, ManagerRole, WalletUserStatus, WalletUserType
from app.dtos.base import BaseDto
from app.dtos.shared.outputs import OwnerInfo


class ManagerAuthResult(BaseDto):

    access_token:str
    access_type:str = "Bearer"

class AccountListItem(BaseDto):
    user_id: int
    full_name: str
    nick_name: Optional[str] = None
    profile_url: Optional[str] = None
    account_type: WalletUserType
    account_status: WalletUserStatus
    phone_no: str
    created_at: datetime
    approved_at: Optional[datetime] = None
    approver_id: Optional[int] = None
    approver_full_name: Optional[str] = None
    current_balance: float
    last_balance: float

class ManagerListItem(BaseDto):
    user_id:int
    full_name:str
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
    full_name:str
    phone_no:int
    district_id:int
    district:str
    township_id:int
    township:str

    last_message_id:int
    last_message:str
    is_last_message_read:bool

class BusinessRequestListItem(BaseDto):
    request_id:int
    qualified_name:str
    description:str
    business_type:BusinessType
    status:BusinessApprovalStatus
    banner_url:Optional[str] = None
    requested_at:datetime
    owner:OwnerInfo