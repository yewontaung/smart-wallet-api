from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.data.database import get_session
from app.dtos.shared.searches import TransactionSearch
from app.services import transaction_service


router = APIRouter(prefix="/transactions")

@router.get("/")
def search(
    search:TransactionSearch = Depends(),
    page:int = Query(ge=1, default=1),
    size:int = Query(ge=10, default=10),
    session:Session = Depends(get_session)
):
    return transaction_service.search(search, page, size, session)

@router.get("/{trx_id}")
def detail(trx_id:UUID, session:Session = Depends(get_session)):

    return transaction_service.find_by_id(trx_id, session)