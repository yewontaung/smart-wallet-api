from uuid import UUID

from sqlmodel import Session

from app.dtos.base import PageResult
from app.dtos.shared.outputs import TransactionListItem
from app.dtos.shared.searches import TransactionSearch


def search(search:TransactionSearch, page:int, size:int, session:Session):
    return

def find_by_id(trx_id:UUID, session:Session) -> PageResult[TransactionListItem]:

    return