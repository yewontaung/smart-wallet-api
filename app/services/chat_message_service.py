from sqlmodel import Session

from app.dtos.base import PageResult
from app.dtos.shared.outputs import ChatMessageListItem
from app.dtos.shared.searches import MessageSearch


def find_by_chat_id(search:MessageSearch, chat_id:int, page:int, size:int, session:Session) -> PageResult[ChatMessageListItem]:
    return