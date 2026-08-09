from datetime import datetime
from typing import Optional

from app.dtos.base import BaseDto


class TransactionSearch(BaseDto):

    q:Optional[str] = None # full name, note

    operation_id:Optional[int] = None

    from_amount:Optional[float] = None
    to_amount:Optional[float] = None

    from_date:Optional[datetime] = None
    to_date:Optional[datetime] = None