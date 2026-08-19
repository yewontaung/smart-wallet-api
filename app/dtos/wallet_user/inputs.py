from typing import Optional

from pydantic import Field

from app.data.enums import BusinessType
from app.dtos.base import BaseDto
from app.dtos.shared.inputs import AddressForm, NRCForm


class WalletUserForm(BaseDto):
    full_name:str
    phone_no:str
    nrc_form:NRCForm
    address_form:AddressForm
    pin:str
    confirm_pin:str

class WalletUserRememberForm(BaseDto):
    rememberToken:str
    pin:str = Field(min_length=6, max_length=6)

class WalletUserSignInForm(BaseDto):
    phone_no:str

class WalletUserVerificationForm(BaseDto):
    verification_token:str
    pin:str

class BusinessProfileForm(BaseDto):
    qualified_name:str 
    description:str
    banner_url:Optional[str] = Field(default=None)
    business_type:BusinessType
