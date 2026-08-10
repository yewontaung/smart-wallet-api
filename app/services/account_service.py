from sqlmodel import Session

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
    return