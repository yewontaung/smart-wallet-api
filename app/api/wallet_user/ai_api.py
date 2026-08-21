from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import Authentication
from app.dtos.wallet_user.inputs import AIMessageForm
from app.services.action import ai_service


router = APIRouter(prefix="/ai")

@router.post("/message")
async def ask(
    auth_user:Authentication,
    form:AIMessageForm,
    session:Session = Depends(get_session)
):
    return await ai_service.ask(form, auth_user.user_id, session)
