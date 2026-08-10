from datetime import datetime
from typing import Optional

from app.data.enums import ManagerRole, WalletUserType
from app.dtos.base import BaseDto


class ManagerSearch(BaseDto):
    q:Optional[str] = None # phone no., email, full name
    role:Optional[ManagerRole] = None
    is_disable:Optional[bool] = None
    created_from:Optional[datetime] = None
    created_to:Optional[datetime] = None

class AccountSearch(BaseDto):
    q:Optional[str] = None # phone no., full name, nick name
    account_type:Optional[WalletUserType] = None
    created_from:Optional[datetime] = None
    created_to:Optional[datetime] = None
    balance_from:Optional[float] = None
    balance_to:Optional[float] = None
    district_id:Optional[int] = None

class ChatSearch(BaseDto):
    q:Optional[str] = None # full name, phone no., nick name
    district_id:Optional[int] = None
