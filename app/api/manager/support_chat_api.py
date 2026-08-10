from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.data.database import get_session
from app.dtos.manager.searches import ChatSearch
from app.dtos.shared.searches import MessageSearch
from app.services import chat_message_service, support_chat_service


router = APIRouter(prefix="/support-chats")

@router.get("/")
def search(
    search:ChatSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session),
):
    return support_chat_service.search(search, page, size, session)

@router.get("/{chat_id}/messages")
def messages(
    chat_id:int,
    search:MessageSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session),
):
    return chat_message_service.find_by_chat_id(search, chat_id, page, size, session)