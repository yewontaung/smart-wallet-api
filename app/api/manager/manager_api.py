from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import ManagerAuthentication
from app.dtos.manager.inputs import ManagerForm
from app.dtos.manager.searches import ManagerSearch
from app.services import manager_service


router = APIRouter("/managers")

@router.get("/")
def search(
    search:ManagerSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session)
):

    return manager_service.search(search, page, size, session)

@router.post("/")
def add_manager(
    form:ManagerForm,
    auth_user:ManagerAuthentication,
    session:Session = Depends(get_session),
):

    return manager_service.add_manager(form, auth_user.user_id, session)