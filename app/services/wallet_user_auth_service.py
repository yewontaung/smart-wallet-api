from sqlmodel import Session, select

from app.data.database import safe_call
from app.data.enums import WalletUserType
from app.data.models import WalletUserAccount
from app.dtos.wallet_user.inputs import WalletUserSignInForm, WalletUserVerificationForm
from app.dtos.wallet_user.outputs import SignInResult, WalletUserAuthResult
from app.utils.cache import InMemoryCache
from app.utils.encryption import encode_jwt
from app.utils.exceptions import BusinessException
from app.utils.hashing import hash_password


wallet_sing_in_cache = InMemoryCache()

def sign_in(form:WalletUserSignInForm, session:Session) -> SignInResult:
    wallet_user = safe_call(
        session.exec(
            select(WalletUserAccount)
            .where(
                WalletUserAccount.phone_no == form.phone_no
            ))
        .first()
        ,"WalletUserAccount", "phone_no", form.phone_no)

    payload = {
        "account_id": wallet_user.account_id,
        "phone_no": wallet_user.phone_no,
    }

    token = encode_jwt(payload)

    verification_token = hash_password(token)
    wallet_sing_in_cache.store(verification_token, payload)
    
    return SignInResult(
        verification_token=verification_token,
    )

def verify_sign_in(form:WalletUserVerificationForm, session:Session) -> WalletUserAuthResult:
    if not form.verification_token in wallet_sing_in_cache.storage:
        raise BusinessException("Invalid token.")
    payload:dict = wallet_sing_in_cache.pop(form.verification_token)
    phone_no = payload.get("phone_no")
    wallet_user = safe_call(
        session.exec(
            select(WalletUserAccount)
            .where(
                WalletUserAccount.phone_no == phone_no
            ))
        .first()
        ,"WalletUserAccount", "phone_no", phone_no)

    if wallet_user.pin != form.pin:
        raise BusinessException("Wrong pin.")

    account = wallet_user.account

    return WalletUserAuthResult(
        access_token=encode_jwt(payload),
        account_id=wallet_user.account_id,
        full_name=account.full_name,
        role="normal-wallet-user" if wallet_user.account_type == WalletUserType.NORMAL else "special-wallet-user",
        phone=wallet_user.phone_no,
    )