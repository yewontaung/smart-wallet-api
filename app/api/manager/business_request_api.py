from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import ManagerAuthentication
from app.dtos.manager.inputs import BusinessRequestRejectForm
from app.dtos.shared.searches import BusinessProfileSearch
from app.services import business_request_service


router = APIRouter(prefix="/business-requests")

@router.get("/")
def search(
    search:BusinessProfileSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session)
):
    return business_request_service.search(search, page, size, session)

@router.put("/{request_id}/reject")
def reject(request_id:int, form:BusinessRequestRejectForm, auth:ManagerAuthentication, session:Session = Depends(get_session)):
    return business_request_service.reject(form, request_id, auth.user_id, session)

@router.post("/{request_id}")
def approve(request_id:int, auth:ManagerAuthentication, session:Session = Depends(get_session)):
    return business_request_service.approve(request_id, auth.user_id, session)

