from app.dtos.base import BaseDto


class NRCForm(BaseDto):
    district_code:str
    township_code:str
    nrc_type:str
    nrc_no:str

class AddressForm(BaseDto):
    address_content:str
    township_id:int
    district_id:int