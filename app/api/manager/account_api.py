from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.data.database import get_session
from app.dtos.shared.searches import TransactionSearch
from app.services import transaction_log_service

router = APIRouter(prefix="/accounts")

@router.get("{account_id}/transaction-logs")
def transactions(
    account_id:int,
    search:TransactionSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session)
):
    return transaction_log_service.search_by_account_id(search, account_id, page, size, session)

@router.get("/{account_id}")
def detail():
    return