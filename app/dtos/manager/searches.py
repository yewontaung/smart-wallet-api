from datetime import datetime
from typing import Optional

from app.data.enums import ManagerRole
from app.dtos.base import BaseDto


class ManagerSearch(BaseDto):
    q:Optional[str] = None # phone no., email, full name
    role:Optional[ManagerRole] = None
    created_from:Optional[datetime] = None