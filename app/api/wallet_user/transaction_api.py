from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import Authentication
from app.services import transaction_service


router = APIRouter(prefix="/transactions")

@router.get("/{trx_id}")
def detail(trx_id:UUID, auth_user:Authentication , session:Session = Depends(get_session)):
    result = transaction_service.find_by_id(trx_id, session)
    if result.receiver_wallet.user_id != auth_user.user_id and result.sender_wallet.user_id != auth_user.user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail={
                "message": "You cannot access this information."
            }
        )
    return result