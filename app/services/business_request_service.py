from sqlalchemy.orm import selectinload
from sqlmodel import Session, desc, func, or_, select

from app.data.models import Account, BusinessApprovalRequest, WalletUserAccount
from app.dtos.base import ModificationResult, PageResult
from app.dtos.manager.inputs import BusinessRequestRejectForm, BusinessRequestStatusChangeForm
from app.dtos.manager.outputs import BusinessRequestListItem
from app.dtos.shared.searches import BusinessProfileSearch


def search(search:BusinessProfileSearch, page:int, size:int, session:Session) -> PageResult[BusinessRequestListItem]:
    QUERY = select(BusinessApprovalRequest).options(
        selectinload(BusinessApprovalRequest.owner)
            .selectinload(WalletUserAccount.account)
    )
    QUERY = search.where(
        QUERY, BusinessApprovalRequest, Account
    ).order_by(
        desc(BusinessApprovalRequest.created_at)
    ).limit(size).offset((page - 1) * size)

    COUNT = select(
        func.count(BusinessApprovalRequest.request_id)
    ).join(
        WalletUserAccount, WalletUserAccount.account_id == BusinessApprovalRequest.owner_id
    ).join(
        Account, Account.account_id == WalletUserAccount.account_id
    )
    COUNT = search.where(COUNT, BusinessApprovalRequest, Account)

    total = session.exec(COUNT).one_or_none() or 0

    result = session.exec(QUERY).all()
    items = [BusinessRequestListItem.from_(item) for item in result]
    return PageResult(
        items=items,
        page=page,
        size=size,
        total=total,
    )

def search_by_owner_id(search:BusinessProfileSearch, user_id:int, page:int, size:int, session:Session) -> PageResult[BusinessRequestListItem]:
    QUERY = select(BusinessApprovalRequest).options(
        selectinload(BusinessApprovalRequest.owner)
            .selectinload(WalletUserAccount.account)
    ).where(BusinessApprovalRequest.owner_id == user_id)

    QUERY = search.where(
        QUERY, BusinessApprovalRequest, Account
    ).order_by(
        desc(BusinessApprovalRequest.created_at)
    ).limit(size).offset((page - 1) * size)

    COUNT = select(
        func.count(BusinessApprovalRequest.request_id)
    ).join(
        WalletUserAccount, WalletUserAccount.account_id == BusinessApprovalRequest.owner_id
    ).join(
        Account, Account.account_id == WalletUserAccount.account_id
    ).where(
        BusinessApprovalRequest.owner_id == user_id
    )
    COUNT = search.where(COUNT, BusinessApprovalRequest, Account)

    total = session.exec(COUNT).one_or_none() or 0

    result = session.exec(QUERY).all()
    items = [BusinessRequestListItem.from_(item) for item in result]
    return PageResult(
        items=items,
        page=page,
        size=size,
        total=total,
    )

def approve(request_id:int, manager_id:int, session:Session) -> ModificationResult:
    return

def reject(form:BusinessRequestRejectForm, request_id:int, manager_id:int, session:Session) -> ModificationResult:
    return

def change_status(form:BusinessRequestStatusChangeForm, request_id:int, manager_id:int, session:Session) -> ModificationResult:
    return