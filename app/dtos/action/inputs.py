from pydantic import Field

from app.dtos.base import BaseDto


class SendMoneyForm(BaseDto):
    amount:float = Field(ge=1)
    sender_wallet_id:int
    receiver_wallet_id:int

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
