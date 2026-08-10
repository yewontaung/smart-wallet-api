from sqlmodel import Session

from app.dtos.base import PageResult
from app.dtos.manager.outputs import SupportChatListItem
from app.dtos.manager.searches import ChatSearch


def search(search:ChatSearch, page:int, size:int, session:Session) -> PageResult[SupportChatListItem]:
    return