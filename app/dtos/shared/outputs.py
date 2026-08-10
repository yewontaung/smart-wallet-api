from datetime import datetime
from typing import Optional
from uuid import UUID

from app.data.enums import BusinessStatus, BusinessType, TransactionStatus, TransactionType, WalletUserType
from app.dtos.base import BaseDto


class WalletInfo(BaseDto):
    wallet_id:int
    user_id:int
    phone_no:str
    full_name:str
    account_type:Optional[WalletUserType] = None


class TransactionListItem(BaseDto):
    trx_id:UUID
    amount:float
    status:TransactionStatus
    note:Optional[str]
    operation:str

    receiver_wallet:WalletInfo
    sender_wallet:WalletInfo

    created_at:datetime
    updated_at:datetime

class TransactionLogListItem(BaseDto):
    log_id:UUID
    trx_id:UUID
    trx_type:TransactionType
    amount:float
    status:TransactionStatus
    note:Optional[str]
    operation:str

    user_id:int
    wallet_info:WalletInfo # actor who send or receive
    created_at:datetime

class AddressInfo(BaseDto):
    address_id:int
    address_content:str
    township:str
    district:str

class ApproverInfo(BaseDto):
    approver_id:int
    approved_at:datetime
    approver_full_name:str

class NRCInfo(BaseDto):
    nrc_id:int
    district_code:str
    township_code:str
    nrc_type:str
    nrc_no:str

class AccountDetail(BaseDto):
    user_id:int
    full_name:str
    nick_name:Optional[str] = None
    profile_url:Optional[str] = None
    account_type:WalletUserType
    phone_no:str
    created_at:datetime
    updated_at:datetime
    current_balance:float
    last_balance:float
    approver:ApproverInfo
    address:AddressInfo
    nrc:NRCInfo

class OwnerInfo(BaseDto):
    user_id:int
    full_name:int
    profile_url:Optional[str] = None


class BusinessProfileListItem(BaseDto):
    business_id:int
    qualify_name:str
    banner_url:str
    description:str
    business_type:BusinessType
    created_at:datetime
    status:BusinessStatus

    owner:OwnerInfo
    approver:ApproverInfo

class TransactionDetail(BaseDto):
    trx_id:UUID
    amount:float
    status:TransactionStatus
    note:Optional[str]
    operation:str

    receiver_wallet:WalletInfo
    sender_wallet:WalletInfo

    created_at:datetime
    updated_at:datetime

class ChatMessageListItem(BaseDto):
    message_id:int
    message_content:str
    created_at:datetime
    updated_at:datetime
    is_read:bool
    chat_id:int
    user_id:int
    user_name:str