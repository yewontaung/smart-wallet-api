from typing import Optional

from pydantic import EmailStr, Field

from app.data.enums import ManagerRole
from app.dtos.base import BaseDto
from app.dtos.enums import SignInWith
from app.dtos.shared.inputs import AddressForm, NRCForm


class ManagerForm(BaseDto):
    full_name:str
    phone_no:str
    account_email:EmailStr
    password:str
    role:ManagerRole
    profile_url:Optional[str] = Field(default=None)

    nrc_form:NRCForm
    address_form:AddressForm


class ManagerSignInForm(BaseDto):
    account_email:EmailStr
    password:str = Field(min_length=6)
    sign_in_with:SignInWith = Field(default=SignInWith.EMAIL)