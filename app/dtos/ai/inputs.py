from typing import Optional

from app.dtos.base import BaseDto


class TransferMoneyRequest(BaseDto):
    receiver:Optional[str] = None
    amount:Optional[str] = None

class MobileTopupRequest(BaseDto):
    phone_number:Optional[str] = None
    amount:Optional[str] = None
