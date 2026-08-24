from datetime import datetime
from typing import Optional

from app.data.enums import BusinessApprovalStatus, BusinessType, ManagerRole, WalletUserStatus, WalletUserType
from app.data.models import BusinessApprovalRequest
from app.dtos.base import BaseDto
from app.dtos.shared.outputs import ApproverInfo, OwnerInfo


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

    @staticmethod
    def from_(item:BusinessApprovalRequest) -> "BusinessRequestListItem":
        account = item.owner.account
        return BusinessRequestListItem(
            request_id=item.request_id,
            qualified_name=item.qualified_name,
            description=item.description,
            business_type=item.business_type,
            status=item.status,
            banner_url=item.banner_url,
            requested_at=item.created_at,
            owner=OwnerInfo(
                user_id=account.account_id,
                full_name=account.full_name,
                profile_url=account.profile_url,
            )
        )

class BusinessProfileDetail(BaseDto):
    business_id:int
    qualified_name:str
    banner_url:Optional[str]
    description:str
    created_at:datetime
    status:BusinessApprovalStatus
    owner:OwnerInfo
    approver:ApproverInfo
