from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import Authentication
from app.dtos.shared.searches import BusinessProfileSearch, TransactionSearch
from app.services import account_service, business_request_service, transaction_log_service, business_service

router = APIRouter(prefix="/me")

@router.get("/")
def index(
    auth_user:Authentication,
    session:Session = Depends(get_session),
):
    return account_service.find_by_account_id(auth_user.user_id, session)

@router.get("/balance")
def balance(auth_user:Authentication, session:Session = Depends(get_session)):
    return account_service.get_balance_by_account_id(auth_user.user_id, session)

@router.get("/profile")
def profile(
    auth_user:Authentication,
    session:Session = Depends(get_session),
):
    return account_service.profile_by_account_id(auth_user.user_id, session)

@router.get("/transaction-logs")
def transaction_logs(
    auth_user:Authentication,
    search:TransactionSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session)
):
    return transaction_log_service.search_by_account_id(search, auth_user.user_id, page, size, session)

@router.get("/businesses")
def businesses(
    auth_user:Authentication,
    search:BusinessProfileSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session),
):
    return business_service.search_by_owner_id(search, auth_user.user_id, page, size, session)

@router.get("/business-requests")
def business_requests(
    auth_user:Authentication,
    search:BusinessProfileSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session),
):
    return business_request_service.search_by_owner_id(search, auth_user.user_id, page, size, session)