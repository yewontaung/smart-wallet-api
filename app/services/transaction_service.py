from uuid import UUID

from sqlalchemy.orm import aliased
from sqlmodel import Session, func, select

from app.data.models import (
    Account,
    Transaction,
    Wallet,
    WalletOperation,
    WalletUserAccount,
)
from app.dtos.base import PageResult
from app.dtos.shared.outputs import TransactionDetail, TransactionListItem, WalletInfo
from app.dtos.shared.searches import TransactionSearch


def search(
    search: TransactionSearch,
    page: int,
    size: int,
    session: Session,
) -> PageResult[TransactionListItem]:

    # =========================================================
    # 1. Aliases for sender and receiver
    # =========================================================

    SenderWallet = aliased(Wallet)
    ReceiverWallet = aliased(Wallet)

    SenderUser = aliased(WalletUserAccount)
    ReceiverUser = aliased(WalletUserAccount)

    SenderAccount = aliased(Account)
    ReceiverAccount = aliased(Account)

    # =========================================================
    # 2. Base query
    # =========================================================

    statement = (
        select(
            Transaction,
            WalletOperation,
            SenderWallet,
            ReceiverWallet,
            SenderUser,
            ReceiverUser,
            SenderAccount,
            ReceiverAccount,
        )
        .join(
            WalletOperation,
            Transaction.operation_id == WalletOperation.operation_id,
        )
        .join(
            SenderWallet,
            Transaction.sender_wallet_id == SenderWallet.wallet_id,
        )
        .join(
            ReceiverWallet,
            Transaction.receiver_wallet_id == ReceiverWallet.wallet_id,
        )
        .join(
            SenderUser,
            SenderWallet.wallet_account_id == SenderUser.account_id,
        )
        .join(
            ReceiverUser,
            ReceiverWallet.wallet_account_id == ReceiverUser.account_id,
        )
        .join(
            SenderAccount,
            SenderUser.account_id == SenderAccount.account_id,
        )
        .join(
            ReceiverAccount,
            ReceiverUser.account_id == ReceiverAccount.account_id,
        )
    )

    # =========================================================
    # 3. q search
    #
    # Search:
    # - sender full name
    # - receiver full name
    # - sender phone number
    # - receiver phone number
    # - transaction note
    # =========================================================

    if search.q:
        search_pattern = f"%{search.q}%"

        statement = statement.where(
            (SenderAccount.full_name.ilike(search_pattern))
            | (ReceiverAccount.full_name.ilike(search_pattern))
            | (SenderUser.phone_no.ilike(search_pattern))
            | (ReceiverUser.phone_no.ilike(search_pattern))
            | (Transaction.note.ilike(search_pattern))
        )

    # =========================================================
    # 4. Operation filter
    # =========================================================

    if search.operation_id is not None:
        statement = statement.where(
            Transaction.operation_id == search.operation_id
        )

    # =========================================================
    # 5. Amount filters
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
    # 6. Date filters
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
    # 7. Count
    # =========================================================

    count_statement = select(func.count()).select_from(
        statement.subquery()
    )

    total = session.exec(count_statement).one()

    # =========================================================
    # 8. Pagination
    # =========================================================

    page = max(page, 1)
    size = max(size, 1)

    offset = (page - 1) * size

    statement = (
        statement
        .order_by(Transaction.created_at.desc())
        .offset(offset)
        .limit(size)
    )

    results = session.exec(statement).all()

    # =========================================================
    # 9. Build response
    # =========================================================

    items = []

    for (
        transaction,
        operation,
        sender_wallet,
        receiver_wallet,
        sender_user,
        receiver_user,
        sender_account,
        receiver_account,
    ) in results:

        sender_wallet_info = WalletInfo(
            wallet_id=sender_wallet.wallet_id,
            user_id=sender_account.account_id,
            phone_no=sender_user.phone_no,
            full_name=sender_account.full_name,
            account_type=sender_user.account_type,
        )

        receiver_wallet_info = WalletInfo(
            wallet_id=receiver_wallet.wallet_id,
            user_id=receiver_account.account_id,
            phone_no=receiver_user.phone_no,
            full_name=receiver_account.full_name,
            account_type=receiver_user.account_type,
        )

        items.append(
            TransactionListItem(
                trx_id=transaction.trx_id,
                amount=transaction.amount,
                status=transaction.status,
                note=transaction.note,
                operation=operation.operation_name,
                receiver_wallet=receiver_wallet_info,
                sender_wallet=sender_wallet_info,
                created_at=transaction.created_at,
                updated_at=transaction.updated_at,
            )
        )

    # =========================================================
    # 10. Return
    # =========================================================

    return PageResult[TransactionListItem](
        items=items,
        page=page,
        size=size,
        total=total,
    )


def find_by_id(
    trx_id: UUID,
    session: Session,
) -> TransactionDetail:

    # =========================================================
    # 1. Aliases for sender and receiver
    # =========================================================

    SenderWallet = aliased(Wallet)
    ReceiverWallet = aliased(Wallet)

    SenderUser = aliased(WalletUserAccount)
    ReceiverUser = aliased(WalletUserAccount)

    SenderAccount = aliased(Account)
    ReceiverAccount = aliased(Account)

    # =========================================================
    # 2. Find transaction
    # =========================================================

    statement = (
        select(
            Transaction,
            WalletOperation,
            SenderWallet,
            ReceiverWallet,
            SenderUser,
            ReceiverUser,
            SenderAccount,
            ReceiverAccount,
        )
        .join(
            WalletOperation,
            Transaction.operation_id == WalletOperation.operation_id,
        )
        .join(
            SenderWallet,
            Transaction.sender_wallet_id == SenderWallet.wallet_id,
        )
        .join(
            ReceiverWallet,
            Transaction.receiver_wallet_id == ReceiverWallet.wallet_id,
        )
        .join(
            SenderUser,
            SenderWallet.wallet_account_id == SenderUser.account_id,
        )
        .join(
            ReceiverUser,
            ReceiverWallet.wallet_account_id == ReceiverUser.account_id,
        )
        .join(
            SenderAccount,
            SenderUser.account_id == SenderAccount.account_id,
        )
        .join(
            ReceiverAccount,
            ReceiverUser.account_id == ReceiverAccount.account_id,
        )
        .where(
            Transaction.trx_id == trx_id
        )
    )

    result = session.exec(statement).first()

    if result is None:
        raise ValueError(
            f"Transaction with id {trx_id} not found"
        )

    (
        transaction,
        operation,
        sender_wallet,
        receiver_wallet,
        sender_user,
        receiver_user,
        sender_account,
        receiver_account,
    ) = result

    # =========================================================
    # 3. Sender wallet information
    # =========================================================

    sender_wallet_info = WalletInfo(
        wallet_id=sender_wallet.wallet_id,
        user_id=sender_account.account_id,
        phone_no=sender_user.phone_no,
        full_name=sender_account.full_name,
        account_type=sender_user.account_type,
    )

    # =========================================================
    # 4. Receiver wallet information
    # =========================================================

    receiver_wallet_info = WalletInfo(
        wallet_id=receiver_wallet.wallet_id,
        user_id=receiver_account.account_id,
        phone_no=receiver_user.phone_no,
        full_name=receiver_account.full_name,
        account_type=receiver_user.account_type,
    )

    # =========================================================
    # 5. Return transaction detail
    # =========================================================

    return TransactionDetail(
        trx_id=transaction.trx_id,
        amount=transaction.amount,
        status=transaction.status,
        note=transaction.note,
        operation=operation.operation_name,
        receiver_wallet=receiver_wallet_info,
        sender_wallet=sender_wallet_info,
        created_at=transaction.created_at,
        updated_at=transaction.updated_at,
    )