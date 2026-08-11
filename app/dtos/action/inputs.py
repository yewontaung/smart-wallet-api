from typing import Optional

from pydantic import Field

from app.dtos.base import BaseDto


class SendMoneyForm(BaseDto):
    amount:float = Field(ge=1)
    sender_wallet_id:int
    receiver_wallet_id:int
    note:Optional[str] = None

    def sorted_wallet(self) -> list[int]:
        return sorted([self.sender_wallet_id, self.receiver_wallet_id])

class PayBillForm(BaseDto):
    amount:float = Field(ge=1)
    sender_wallet_id:int
    receiver_wallet_id:int
    business_id:int

class MobileTopUpForm(BaseDto):
    amount:float = Field(ge=1000)
    phone_no:str = Field(min_length=5)
    sender_wallet_id:int
    receiver_wallet_id:int
    business_id:int
