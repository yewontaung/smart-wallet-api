from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.data.database import get_session
from app.dtos.wallet_user.inputs import WalletUserForm, WalletUserRememberForm, WalletUserSignInForm, WalletUserVerificationForm
from app.services import account_service, wallet_user_auth_service


router = APIRouter(prefix="/auth")

@router.post("/remember")
def remeber(form:WalletUserRememberForm, session:Session = Depends(get_session)):
    return wallet_user_auth_service.remember(form, session)

@router.post("/sign-up")
def sign_up(form:WalletUserForm, session:Session = Depends(get_session)):
    return account_service.create_wallet_user_account(form, session)

@router.post("/sign-in")
def sign_in(form:WalletUserSignInForm, session:Session = Depends(get_session)):
    return wallet_user_auth_service.sign_in(form, session)

@router.post("/sign-in/verify")
def verify(form:WalletUserVerificationForm, session:Session = Depends(get_session)):
    return wallet_user_auth_service.verify_sign_in(form, session)