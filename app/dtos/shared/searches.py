from datetime import datetime
from typing import Optional

from app.data.enums import BusinessType
from app.dtos.base import BaseDto


class TransactionSearch(BaseDto):

    q:Optional[str] = None # full name, note, phone no

    operation_id:Optional[int] = None

    amount_from:Optional[float] = None
    amount_to:Optional[float] = None

    date_from:Optional[datetime] = None
    date_to:Optional[datetime] = None

class BusinessProfileSearch(BaseDto):
    q:Optional[str] = None # owner name, qualify name

    business_type:Optional[BusinessType] = None

    created_from:Optional[datetime] = None
    created_to:Optional[datetime] = None

class MessageSearch(BaseDto):
    q:Optional[str] = None # user name, phone no, message text

    date_from:Optional[datetime] = None
    date_to:Optional[datetime] = None

class LocationSearch(BaseDto):
    q:Optional[str] = None

    users_from:Optional[int] = None
    users_to:Optional[int] = None

    date_from:Optional[datetime] = None
    date_to:Optional[datetime] = None

class ReceiverSearch(BaseDto):
    phone_no:str