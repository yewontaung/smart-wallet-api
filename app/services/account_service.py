from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.data.database import safe_call
from app.data.enums import WalletType
from app.data.models import Wallet, WalletUserAccount
from app.dtos.base import ModificationResult, PageResult
from app.dtos.manager.outputs import AccountListItem
from app.dtos.manager.searches import AccountSearch
from app.dtos.shared.outputs import AccountDetail, ReceiverProfile
from app.dtos.shared.searches import ReceiverSearch
from app.dtos.wallet_user.inputs import WalletUserForm


def search(search:AccountSearch, page:int, size:int, session:Session) -> PageResult[AccountListItem]:
    return

def find_by_account_id(account_id:int, session:Session) -> AccountDetail:
    return

def create_wallet_user_account(form:WalletUserForm, session:Session) -> ModificationResult:
    return

def approve_wallet_user(account_id:int, user_id:int, session:Session) -> ModificationResult:
    return

def search_receiver(search:ReceiverSearch, session:Session) -> ReceiverProfile:
    wallet_user = safe_call(
        session.exec(
            select(WalletUserAccount).options(
                selectinload(WalletUserAccount.account)
            ).where(
                WalletUserAccount.phone_no == search.phone_no
            )
        ).first(), 
        "WalletUserAccount", 
        "phone", 
        search.phone_no)
    
    wallet = safe_call(
        session.exec(
            select(Wallet).where(
                Wallet.wallet_account_id == wallet_user.account_id, 
                Wallet.wallet_type == WalletType.FUNDING
            )
        ).first(),
        "Wallet",
        "account_id",
        wallet_user.account_id
    )

    return ReceiverProfile(
        user_id=wallet_user.account_id,
        wallet_id=wallet.wallet_id,
        full_name=wallet_user.account.full_name,   
        phone_no=wallet_user.phone_no,
    )