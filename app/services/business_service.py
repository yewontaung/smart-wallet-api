from sqlmodel import Session, select, func

from app.data.database import safe_call
from app.data.enums import BusinessApprovalStatus
from app.data.models import (
    Account,
    BusinessApprovalRequest,
    BusinessProfile,
    ManagerAccount,
    Wallet,
    WalletUserAccount,
)
from app.dtos.base import ModificationResult, PageResult
from app.dtos.shared.outputs import (
    ApproverInfo,
    BusinessProfileListItem,
    OwnerInfo,
    ProviderProfile,
)
from app.dtos.shared.searches import BusinessProfileSearch
from app.dtos.wallet_user.inputs import BusinessProfileForm


def _build_business_statement(search: BusinessProfileSearch):
    statement = (
        select(
            BusinessProfile,
            Account.full_name,
            WalletUserAccount.account_id,
            ManagerAccount.account_id,
            ManagerAccount.account_id,
            Account.full_name,
        )
        .join(
            WalletUserAccount,
            WalletUserAccount.account_id == BusinessProfile.owner_id,
        )
        .join(
            Account,
            Account.account_id == WalletUserAccount.account_id,
        )
        .outerjoin(
            ManagerAccount,
            ManagerAccount.account_id == BusinessProfile.approved_by,
        )
        .where(BusinessProfile.is_deleted == False)
    )

    if search.q:
        keyword = f"%{search.q}%"

        statement = statement.where(
            (BusinessProfile.qualified_name.ilike(keyword))
            | (Account.full_name.ilike(keyword))
        )

    if search.business_type:
        statement = statement.where(
            BusinessProfile.business_type == search.business_type
        )

    if search.created_from:
        statement = statement.where(
            BusinessProfile.created_at >= search.created_from
        )

    if search.created_to:
        statement = statement.where(
            BusinessProfile.created_at <= search.created_to
        )

    return statement


def _to_business_list_item(row) -> BusinessProfileListItem:
    (
        business,
        owner_name,
        owner_id,
        approver_id,
        approver_account_id,
        approver_name,
    ) = row

    owner = OwnerInfo(
        user_id=owner_id,
        full_name=owner_name,
        profile_url=None,
    )

    approver = None

    if approver_id is not None:
        approver = ApproverInfo(
            approver_id=approver_id,
            approved_at=business.updated_at,
            approver_full_name=approver_name or "",
        )

    return BusinessProfileListItem(
        business_id=business.business_id,
        qualified_name=business.qualified_name,
        banner_url=business.banner_url,
        description=business.description,
        business_type=business.business_type,
        created_at=business.created_at,
        status=business.status,
        owner=owner,
        approver=approver,
    )


def search(
    search: BusinessProfileSearch,
    page: int,
    size: int,
    session: Session,
) -> PageResult[BusinessProfileListItem]:

    statement = _build_business_statement(search)

    count_statement = select(
        func.count()
    ).select_from(
        statement.subquery()
    )

    total = session.exec(count_statement).one()

    statement = statement.offset(
        (page - 1) * size
    ).limit(size)

    rows = session.exec(statement).all()

    items = [
        _to_business_list_item(row)
        for row in rows
    ]

    return PageResult(
        items=items,
        page=page,
        size=size,
        total=total,
    )


def search_provider_by_id(
    provider_id: int,
    session: Session,
) -> ProviderProfile:

    statement = (
        select(
            BusinessProfile,
            Wallet,
        )
        .join(
            Wallet,
            Wallet.wallet_account_id == BusinessProfile.owner_id,
        )
        .where(
            BusinessProfile.business_id == provider_id,
            BusinessProfile.is_deleted == False,
        )
    )

    result = session.exec(statement).first()

    if not result:
        return None

    business, wallet = result

    return ProviderProfile(
        business_id=business.business_id,
        qualified_name=business.qualified_name,
        wallet_id=wallet.wallet_id,
    )


def search_by_owner_id(
    search: BusinessProfileSearch,
    user_id: int,
    page: int,
    size: int,
    session: Session,
) -> PageResult[BusinessProfileListItem]:

    statement = _build_business_statement(search)

    statement = statement.where(
        BusinessProfile.owner_id == user_id
    )

    count_statement = select(
        func.count()
    ).select_from(
        statement.subquery()
    )

    total = session.exec(count_statement).one()

    statement = statement.offset(
        (page - 1) * size
    ).limit(size)

    rows = session.exec(statement).all()

    items = [
        _to_business_list_item(row)
        for row in rows
    ]

    return PageResult(
        items=items,
        page=page,
        size=size,
        total=total,
    )


def apply_request(
    form: BusinessProfileForm,
    user_id: int,
    session: Session,
) -> ModificationResult:

    wallet_user = safe_call(session.get(WalletUserAccount, user_id), "WalletUserAccount", "account_id", user_id)
    business_request = BusinessApprovalRequest(
        qualified_name=form.qualified_name,
        banner_url=form.banner_url,
        business_type=form.business_type,
        description=form.description,
        owner_id=wallet_user.account_id,
        status=BusinessApprovalStatus.PENDING,
    )

    session.add(business_request)
    session.commit()
    session.refresh(business_request)

    return ModificationResult(
        result_item=business_request.request_id,
        is_success=True,
        message="Business profile is requested successfully.",
    )