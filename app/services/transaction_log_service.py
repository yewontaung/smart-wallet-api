from sqlmodel import Session, func, select

from app.data.models import (
    Account,
    Transaction,
    TransactionLog,
    Wallet,
    WalletOperation,
    WalletUserAccount,
)
from app.dtos.base import PageResult
from app.dtos.shared.outputs import TransactionLogListItem, WalletInfo
from app.dtos.shared.searches import TransactionSearch


def search_by_account_id(
    search: TransactionSearch,
    account_id: int,
    page: int,
    size: int,
    session: Session,
) -> PageResult[TransactionLogListItem]:

    # =========================================================
    # Base query
    # =========================================================

    statement = (
        select(
            TransactionLog,
            Transaction,
            Wallet,
            WalletUserAccount,
            Account,
            WalletOperation,
        )
        .join(
            Transaction,
            TransactionLog.trx_id == Transaction.trx_id,
        )
        .join(
            Wallet,
            TransactionLog.wallet_id == Wallet.wallet_id,
        )
        .join(
            WalletUserAccount,
            Wallet.wallet_account_id == WalletUserAccount.account_id,
        )
        .join(
            Account,
            WalletUserAccount.account_id == Account.account_id,
        )
        .join(
            WalletOperation,
            Transaction.operation_id == WalletOperation.operation_id,
        )
        .where(
            Wallet.wallet_account_id == account_id,
        )
    )

    # =========================================================
    # q - full name, phone number, or transaction note
    # =========================================================

    if search.q:
        search_pattern = f"%{search.q}%"

        statement = statement.where(
            (Account.full_name.ilike(search_pattern))
            | (WalletUserAccount.phone_no.ilike(search_pattern))
            | (Transaction.note.ilike(search_pattern))
        )

    # =========================================================
    # Operation filter
    # =========================================================

    if search.operation_id is not None:
        statement = statement.where(
            Transaction.operation_id == search.operation_id
        )

    # =========================================================
    # Amount filters
    # =========================================================

    if search.amount_from is not None:
        statement = statement.where(
            Transaction.amount >= search.amount_from
        )

    if search.amount_to is not None:
        statement = statement.where(
            Transaction.amount <= search.amount_to
        )

    # =========================================================
    # Date filters
    # =========================================================

    if search.date_from is not None:
        statement = statement.where(
            Transaction.created_at >= search.date_from
        )

    if search.date_to is not None:
        statement = statement.where(
            Transaction.created_at <= search.date_to
        )

    # =========================================================
    # Count total matching records
    # =========================================================

    count_statement = select(func.count()).select_from(
        statement.subquery()
    )

    total = session.exec(count_statement).one()

    # =========================================================
    # Pagination
    # =========================================================

    offset = (page - 1) * size

    statement = (
        statement
        .order_by(TransactionLog.created_at.desc())
        .offset(offset)
        .limit(size)
    )

    results = session.exec(statement).all()

    # =========================================================
    # Build response items
    # =========================================================

    items = []

    for (
        transaction_log,
        transaction,
        wallet,
        wallet_user,
        account,
        operation,
    ) in results:

        wallet_info = WalletInfo(
            wallet_id=wallet.wallet_id,
            user_id=account.account_id,
            phone_no=wallet_user.phone_no,
            full_name=account.full_name,
            account_type=wallet_user.account_type,
        )

        items.append(
            TransactionLogListItem(
                log_id=transaction_log.log_id,
                trx_id=transaction.trx_id,
                trx_type=transaction_log.trx_type,
                amount=transaction.amount,
                status=transaction.status,
                note=transaction.note,
                operation=operation.operation_name,
                user_id=account.account_id,
                wallet_info=wallet_info,
                created_at=transaction_log.created_at,
            )
        )

    # =========================================================
    # Return paginated result
    # =========================================================

    return PageResult[TransactionLogListItem](
        items=items,
        page=page,
        size=size,
        total=total,
    )