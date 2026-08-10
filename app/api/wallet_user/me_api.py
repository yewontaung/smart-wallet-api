from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import WalletUserAuthentication
from app.dtos.shared.searches import BusinessProfileSearch, TransactionSearch
from app.services import account_service, transaction_log_service, business_service

router = APIRouter(prefix="/me")

@router.get("/")
def index(
    auth_user:WalletUserAuthentication,
    session:Session = Depends(get_session),
):
    return account_service.find_by_account_id(auth_user.user_id, session)

@router.get("/transaction-logs")
def transaction_logs(
    auth_user:WalletUserAuthentication,
    search:TransactionSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session)
):
    return transaction_log_service.search_by_account_id(search, auth_user.user_id, page, size, session)

@router.get("/businesses")
def businesses(
    auth_user:WalletUserAuthentication,
    search:BusinessProfileSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session),
):
    return business_service.search_by_owner_id(search, auth_user.user_id, page, size, session)