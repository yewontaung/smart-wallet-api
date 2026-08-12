from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload

from app.data.models import (
    Account,
    Address,
    ManagerAccount,
    NRC,
    Wallet,
    WalletUserAccount,
)
from app.data.meta_models import Township
from app.data.database import safe_call
from app.data.enums import WalletType

from app.dtos.base import ModificationResult, PageResult
from app.dtos.manager.outputs import AccountListItem
from app.dtos.manager.searches import AccountSearch
from app.dtos.shared.outputs import (
    AccountDetail,
    ReceiverProfile,
    AddressInfo,
    NRCInfo,
    ApproverInfo,
)
from app.dtos.shared.searches import ReceiverSearch
from app.dtos.wallet_user.inputs import WalletUserForm


# =========================================================
# Search Accounts
# =========================================================

def search(
    search: AccountSearch,
    page: int,
    size: int,
    session: Session,
) -> PageResult[AccountListItem]:

    # ---------------------------------------------------------
    # Base query
    # ---------------------------------------------------------
    statement = (
        select(
            Account,
            WalletUserAccount,
            Wallet,
            ManagerAccount,
        )
        .join(
            WalletUserAccount,
            WalletUserAccount.account_id == Account.account_id,
        )
        .outerjoin(
            Wallet,
            Wallet.wallet_account_id == WalletUserAccount.account_id,
        )
        .outerjoin(
            ManagerAccount,
            ManagerAccount.account_id == WalletUserAccount.approved_by,
        )
    )

    # ---------------------------------------------------------
    # Search keyword
    # Phone number, full name, nickname
    # ---------------------------------------------------------
    if search.q:
        search_pattern = f"%{search.q}%"

        statement = statement.where(
            (Account.full_name.ilike(search_pattern))
            | (WalletUserAccount.nick_name.ilike(search_pattern))
            | (WalletUserAccount.phone_no.ilike(search_pattern))
        )

    # ---------------------------------------------------------
    # Account type
    # ---------------------------------------------------------
    if search.account_type is not None:
        statement = statement.where(
            WalletUserAccount.account_type == search.account_type
        )

    # ---------------------------------------------------------
    # Account status
    # ---------------------------------------------------------
    if search.account_status is not None:
        statement = statement.where(
            WalletUserAccount.account_status == search.account_status
        )

    # ---------------------------------------------------------
    # Created date
    # ---------------------------------------------------------
    if search.created_from is not None:
        statement = statement.where(
            Account.created_at >= search.created_from
        )

    if search.created_to is not None:
        statement = statement.where(
            Account.created_at <= search.created_to
        )

    # ---------------------------------------------------------
    # Balance
    # ---------------------------------------------------------
    if search.balance_from is not None:
        statement = statement.where(
            Wallet.current_balance >= search.balance_from
        )

    if search.balance_to is not None:
        statement = statement.where(
            Wallet.current_balance <= search.balance_to
        )

    # ---------------------------------------------------------
    # District
    #
    # Account
    #   -> Address
    #   -> Township
    #   -> District
    # ---------------------------------------------------------
    if search.district_id is not None:
        statement = (
            statement
            .join(
                Address,
                Address.account_id == Account.account_id,
            )
            .join(
                Township,
                Township.township_id == Address.township_id,
            )
            .where(
                Township.district_id == search.district_id
            )
        )

    # ---------------------------------------------------------
    # Count before pagination
    # ---------------------------------------------------------
    count_statement = select(
        func.count()
    ).select_from(
        statement.subquery()
    )

    total = session.exec(count_statement).one()

    # ---------------------------------------------------------
    # Pagination
    # ---------------------------------------------------------
    page = max(page, 1)
    size = max(size, 1)

    offset = (page - 1) * size

    statement = (
        statement
        .order_by(Account.created_at.desc())
        .offset(offset)
        .limit(size)
    )

    results = session.exec(statement).all()

    # ---------------------------------------------------------
    # Build response
    # ---------------------------------------------------------
    items = []

    for account, wallet_user, wallet, approver in results:

        items.append(
            AccountListItem(
                user_id=account.account_id,
                full_name=account.full_name,
                nick_name=wallet_user.nick_name,
                profile_url=account.profile_url,
                account_type=wallet_user.account_type,
                account_status=wallet_user.account_status,
                phone_no=wallet_user.phone_no,
                created_at=account.created_at,

                approved_at=(
                    wallet_user.approver.updated_at
                    if wallet_user.approver
                    else None
                ),

                approver_id=wallet_user.approved_by,

                approver_full_name=(
                    approver.account.full_name
                    if approver and approver.account
                    else None
                ),

                current_balance=(
                    wallet.current_balance
                    if wallet
                    else 0
                ),

                last_balance=(
                    wallet.last_balance
                    if wallet
                    else 0
                ),
            )
        )

    return PageResult(
        items=items,
        page=page,
        size=size,
        total=total,
    )


# =========================================================
# Find Account By ID
# =========================================================

def find_by_account_id(
    account_id: int,
    session: Session,
) -> AccountDetail:

    # =========================================================
    # 1. Get account
    # =========================================================

    account = session.get(Account, account_id)

    if account is None:
        raise ValueError(
            f"Account with id {account_id} not found"
        )

    # =========================================================
    # 2. Get wallet user account
    # =========================================================

    wallet_user = session.get(
        WalletUserAccount,
        account_id,
    )

    if wallet_user is None:
        raise ValueError(
            f"Wallet user account with id {account_id} not found"
        )

    # =========================================================
    # 3. Get wallet
    # =========================================================

    wallet_statement = (
        select(Wallet)
        .where(
            Wallet.wallet_account_id == account_id
        )
    )

    wallet = session.exec(wallet_statement).first()

    if wallet is None:
        raise ValueError(
            f"Wallet for account {account_id} not found"
        )

    # =========================================================
    # 4. Get NRC
    # =========================================================

    nrc_statement = (
        select(NRC)
        .where(
            NRC.account_id == account_id
        )
    )

    nrc = session.exec(nrc_statement).first()

    if nrc is None:
        raise ValueError(
            f"NRC for account {account_id} not found"
        )

    # =========================================================
    # 5. Get Address
    # =========================================================

    address_statement = (
        select(Address)
        .where(
            Address.account_id == account_id
        )
    )

    address = session.exec(address_statement).first()

    if address is None:
        raise ValueError(
            f"Address for account {account_id} not found"
        )

    # =========================================================
    # 6. Get Township
    # =========================================================

    township = address.township

    if township is None:
        raise ValueError(
            f"Township for address {address.address_id} not found"
        )

    # =========================================================
    # 7. Get District
    # =========================================================

    district = township.district

    if district is None:
        raise ValueError(
            f"District for township {township.township_id} not found"
        )

    # =========================================================
    # 8. Build address info
    # =========================================================

    address_info = AddressInfo(
        address_id=address.address_id,
        address_content=address.address_content,
        township=township.township_name,
        district=district.district_name,
    )

    # =========================================================
    # 9. Build NRC info
    # =========================================================

    nrc_info = NRCInfo(
        nrc_id=nrc.nrc_id,
        district_code=nrc.district_code,
        township_code=nrc.township_code,
        nrc_type=nrc.nrc_type,
        nrc_no=nrc.nrc_no,
    )

    # =========================================================
    # 10. Get approver
    # =========================================================

    approver_info = None

    if wallet_user.approved_by is not None:

        approver_account = session.get(
            ManagerAccount,
            wallet_user.approved_by,
        )

        if approver_account is not None:

            approver_base_account = session.get(
                Account,
                approver_account.account_id,
            )

            if approver_base_account is not None:

                approver_info = ApproverInfo(
                    approver_id=approver_account.account_id,
                    approved_at=wallet_user.updated_at,
                    approver_full_name=(
                        approver_base_account.full_name
                    ),
                )

    # =========================================================
    # 11. Build AccountDetail
    # =========================================================

    return AccountDetail(
        user_id=account.account_id,
        full_name=account.full_name,
        nick_name=wallet_user.nick_name,
        profile_url=account.profile_url,
        account_type=wallet_user.account_type,
        account_status=wallet_user.account_status,
        phone_no=wallet_user.phone_no,
        created_at=account.created_at,
        updated_at=account.updated_at,

        current_balance=wallet.current_balance,
        last_balance=wallet.last_balance,

        approver=approver_info,
        address=address_info,
        nrc=nrc_info,
    )


# =========================================================
# Create Wallet User Account
# =========================================================

def create_wallet_user_account(
    form: WalletUserForm,
    session: Session,
) -> ModificationResult:
    return


# =========================================================
# Approve Wallet User
# =========================================================

def approve_wallet_user(
    account_id: int,
    user_id: int,
    session: Session,
) -> ModificationResult:
    return


# =========================================================
# Search Receiver
# =========================================================

def search_receiver(search:ReceiverSearch, session:Session) -> ReceiverProfile:
    wallet_user = safe_call(
        session.exec(
            select(WalletUserAccount).options(
                selectinload(WalletUserAccount.account)
            ).where(
                WalletUserAccount.phone_no == search.phone_no
            )
        ).first(), 
        "WalletUserAccount", 
        "phone", 
        search.phone_no)
    
    wallet = safe_call(
        session.exec(
            select(Wallet).where(
                Wallet.wallet_account_id == wallet_user.account_id, 
                Wallet.wallet_type == WalletType.FUNDING
            )
        ).first(),
        "Wallet",
        "account_id",
        wallet_user.account_id
    )

    return ReceiverProfile(
        user_id=wallet_user.account_id,
        wallet_id=wallet.wallet_id,
        full_name=wallet_user.account.full_name,   
        phone_no=wallet_user.phone_no,
    )