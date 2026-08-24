from sqlalchemy.orm import selectinload
from sqlmodel import Session, desc, func, or_, select

from app.data.database import safe_call
from app.data.enums import BusinessApprovalStatus, BusinessStatus
from app.data.models import Account, BusinessApprovalRequest, BusinessProfile, ManagerAccount, WalletUserAccount
from app.dtos.base import ModificationResult, PageResult
from app.dtos.manager.inputs import BusinessRequestRejectForm, BusinessRequestStatusChangeForm
from app.dtos.manager.outputs import BusinessRequestListItem
from app.dtos.shared.searches import BusinessProfileSearch
from app.utils.exceptions import BusinessException


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
    manager = safe_call(session.get(ManagerAccount, manager_id), "ManagerAccount", "manager_id", manager_id)
    business_request = safe_call(session.get(BusinessApprovalRequest, request_id), "BusinessApprovalRequest", "request_id", request_id)
    if business_request.status == BusinessApprovalStatus.REJECTED:
        raise BusinessException("Rejected business request cannot be approved.")
    if business_request.status == BusinessApprovalStatus.PENDING:
        raise BusinessException("Pending business request cannot be approved.")

    business_profile = BusinessProfile(
        qualified_name=business_request.qualified_name,
        banner_url=business_request.banner_url,
        description=business_request.description,
        status=BusinessStatus.OPEN,
        owner_id=business_request.owner_id,
        business_type=business_request.business_type,
        approved_by=manager.account_id,
    )

    session.add(business_profile)
    session.delete(business_request)
    session.commit()
    session.refresh(business_profile)

    return ModificationResult(
        result_item=business_profile.business_id,
        is_success=True,
        message=f"Business Profile: {business_profile.qualified_name} is approved."
    )

def reject(form:BusinessRequestRejectForm, request_id:int, manager_id:int, session:Session) -> ModificationResult:
    business_request = safe_call(session.get(BusinessApprovalRequest, request_id), "BusinessApprovalRequest", "request_id", request_id)
    if business_request.status == BusinessApprovalStatus.REJECTED:
        raise BusinessException("Request is already rejected.")
    business_request.status = BusinessApprovalStatus.REJECTED
    business_request.remark = form.remark
    business_request.updated_by = manager_id
    session.commit()
    return ModificationResult(
        result_item=business_request.request_id,
        is_success=True,
        message=f"Business Request : {request_id} is rejected."
    )

def change_status(form:BusinessRequestStatusChangeForm, request_id:int, manager_id:int, session:Session) -> ModificationResult:
    business_request = safe_call(session.get(BusinessApprovalRequest, request_id), "BusinessApprovalRequest", "request_id", request_id)
    if business_request.status == form.status:
        raise BusinessException("New status cannot be old status.")
    business_request.status = form.status
    business_request.updated_by = manager_id
    session.commit()
    return ModificationResult(
        result_item=business_request.request_id,
        is_success=True,
        message=f"Business Request : {request_id} is changed to {form.status}."
    )
