from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import Authentication
from app.dtos.wallet_user.inputs import ContactForm
from app.services import contact_service


router = APIRouter(prefix="/contacts")

@router.get("/")
def index(auth_user:Authentication, session:Session = Depends(get_session)):
    return contact_service.search(account_id=auth_user.user_id, session=session)

@router.post("/")
def add(
    form:ContactForm,
    auth_user:Authentication, 
    session:Session = Depends(get_session)
):
    return contact_service.create(form, auth_user.user_id, session)

@router.delete("/{contact_id}")
def remove(contact_id:UUID, auth_user: Authentication, session:Session = Depends(get_session)):
    return contact_service.remove(contact_id, auth_user.user_id, session)