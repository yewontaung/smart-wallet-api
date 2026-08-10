from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import WalletUserAuthentication
from app.dtos.shared.searches import BusinessProfileSearch
from app.dtos.wallet_user.inputs import BusinessProfileForm
from app.services import business_service

router = APIRouter(prefix="/businesses")

@router.get("/")
def search(
    search:BusinessProfileSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session)
):
    return business_service.search(search, page, size, session)

@router.post("/")
def apply_request(
    form:BusinessProfileForm,
    auth_user:WalletUserAuthentication,
    session:Session = Depends(get_session),
):
    return business_service.apply_request(form, auth_user.user_id, session)
