from sqlmodel import Session

from app.dtos.wallet_user.inputs import WalletUserSignInForm, WalletUserVerificationForm
from app.dtos.wallet_user.outputs import SignInResult, WalletUserAuthResult


def sign_in(form:WalletUserSignInForm, session:Session) -> SignInResult:
    return

def verify_sign_in(form:WalletUserVerificationForm, session:Session) -> WalletUserAuthResult:
    return