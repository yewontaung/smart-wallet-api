from sqlmodel import Session

from app.dtos.base import PageResult
from app.dtos.shared.outputs import TransactionLogListItem


def search_by_account_id(
    search, 
    account_id:int, 
    page:int, 
    size:int, 
    session:Session
) -> PageResult[TransactionLogListItem]:
    return