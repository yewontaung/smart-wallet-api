from datetime import datetime
from typing import Optional

from app.data.enums import BusinessType
from app.dtos.base import BaseDto


class TransactionSearch(BaseDto):

    q:Optional[str] = None # full name, note

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
    