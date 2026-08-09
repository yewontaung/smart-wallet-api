from datetime import datetime
from typing import Optional
from uuid import UUID

from app.data.enums import TransactionStatus, TransactionType, WalletUserType
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
    wallet_info:WalletInfo # actor info
