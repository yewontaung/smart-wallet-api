from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.data.database import get_session
from app.dtos.manager.inputs import ManagerSignInForm
from app.services import manager_auth_service


router = APIRouter(prefix="/auth")

@router.post("/sign-in")
def sign_in(
    form:ManagerSignInForm,
    session:Session = Depends(get_session)
):

    return manager_auth_service.sign_in(form, session)