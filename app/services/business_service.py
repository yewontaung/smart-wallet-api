from sqlmodel import Session

from app.dtos.base import PageResult
from app.dtos.shared.outputs import BusinessProfileListItem
from app.dtos.shared.searches import BusinessProfileSearch


def search(search:BusinessProfileSearch, page:int, size:int, session:Session) -> PageResult[BusinessProfileListItem]:
    return