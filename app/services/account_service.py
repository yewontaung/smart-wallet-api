from sqlmodel import Session

from app.dtos.base import PageResult
from app.dtos.manager.outputs import AccountListItem
from app.dtos.manager.searches import AccountSearch
from app.dtos.shared.outputs import AccountDetail


def search(search:AccountSearch, page:int, size:int, session:Session) -> PageResult[AccountListItem]:
    return

def find_by_account_id(account_id:int, session:Session) -> AccountDetail:
    return