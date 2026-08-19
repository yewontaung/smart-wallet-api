from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import Authentication
from app.dtos.manager.searches import AccountSearch
from app.dtos.shared.searches import TransactionSearch
from app.services import account_service, transaction_log_service

router = APIRouter(prefix="/accounts")

@router.get("/")
def search(
    search:AccountSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session)
):
    return account_service.search(search, page, size, session)

@router.get("/{account_id}/transaction-logs")
def transactions(
    account_id:int,
    search:TransactionSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session)
):
    return transaction_log_service.search_by_account_id(search, account_id, page, size, session)

@router.get("/{account_id}/approve")
def approve_account(account_id:int, session:Session = Depends(get_session)):
    return account_service.approve_wallet_user(account_id, 1, session)

@router.get("/{account_id}")
def detail(
    account_id:int,
    auth_user:Authentication,
    session:Session = Depends(get_session)
):
    
    return account_service.find_by_account_id(account_id, session)