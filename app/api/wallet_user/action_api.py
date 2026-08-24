from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import Authentication
from app.dtos.action.inputs import MobileTopUpForm, PayBillForm, SendMoneyForm
from app.dtos.shared.searches import ReceiverSearch
from app.services import account_service, business_service
from app.services.action import wallet_action_service


router = APIRouter(prefix="/action")

@router.get("/receiver")
def search_receiver(auth_user:Authentication, search:ReceiverSearch = Depends(), session:Session = Depends(get_session)):
    return account_service.search_receiver(search, auth_user.user_id, session)

@router.get("/providers/{provider_id}")
def search_provider(provider_id:int, session:Session = Depends(get_session)):
    return business_service.search_provider_by_id(provider_id, session)

@router.post("/transfer")
def transfer_money(
    form:SendMoneyForm,
    auth_user:Authentication,
    session:Session = Depends(get_session)
):
    return wallet_action_service.send_money(form, auth_user.user_id, session)

@router.post("/pay")
def pay_bill(
    form:PayBillForm, 
    auth_user:Authentication,
    session:Session = Depends(get_session)
):
    return wallet_action_service.pay_bill(form, auth_user.user_id, session)

@router.post("/mobile-topup")
def mobile_topup(
    form:MobileTopUpForm,
    auth_user:Authentication,
    session:Session = Depends(get_session)
):
    return wallet_action_service.top_up(form, auth_user.user_id, session)