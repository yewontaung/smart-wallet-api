from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import Authentication
from app.dtos.manager.inputs import DistrictForm
from app.dtos.shared.searches import LocationSearch
from app.services.resource import district_service


router = APIRouter(prefix="/districts")

@router.get("/")
def search(
    search:LocationSearch = Depends(),
    session:Session = Depends(get_session)
):
    return district_service.search(search, session)

@router.post("/")
def add_district(
    form:DistrictForm,
    auth_user:Authentication,
    session:Session = Depends(get_session)
):
    return district_service.save_district(form, auth_user.user_id, session)