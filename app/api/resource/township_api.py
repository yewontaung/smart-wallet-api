from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import ManagerAuthentication
from app.dtos.manager.inputs import TownshipForm
from app.dtos.shared.searches import LocationSearch
from app.services.resource import township_service


router = APIRouter(prefix="/districts")

@router.get("/")
def search(
    search:LocationSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session)
):
    return township_service.search(search, page, size, session)

@router.post("/")
def add_district(
    form:TownshipForm,
    auth_user:ManagerAuthentication,
    session:Session = Depends(get_session)
):
    return township_service.save_district(form, auth_user.user_id, session)