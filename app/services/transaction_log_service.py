from sqlalchemy.orm import aliased
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
    # 1. Create aliases for sender and receiver
    # =========================================================

    SenderWallet = aliased(Wallet)
    ReceiverWallet = aliased(Wallet)

    SenderUser = aliased(WalletUserAccount)
    ReceiverUser = aliased(WalletUserAccount)

    SenderAccount = aliased(Account)
    ReceiverAccount = aliased(Account)

    # =========================================================
    # 2. Base query
    #
    # TransactionLog.wallet_id is the wallet whose history
    # we are viewing.
    #
    # We separately load sender_wallet and receiver_wallet
    # so that we can return the OTHER wallet in wallet_info.
    # =========================================================

    statement = (
        select(
            TransactionLog,
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
            Transaction,
            TransactionLog.trx_id == Transaction.trx_id,
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
            TransactionLog.wallet_id.in_(
                select(Wallet.wallet_id).where(
                    Wallet.wallet_account_id == account_id
                )
            )
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
    # 7. Count total matching records
    # =========================================================

    count_statement = select(func.count()).select_from(
        statement.subquery()
    )

    total = session.exec(count_statement).one()

    # =========================================================
    # 8. Pagination
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
    # 9. Build response
    # =========================================================

    items = []

    for (
        transaction_log,
        transaction,
        operation,
        sender_wallet,
        receiver_wallet,
        sender_user,
        receiver_user,
        sender_account,
        receiver_account,
    ) in results:

        # =====================================================
        # IMPORTANT:
        #
        # wallet_info MUST contain the OTHER wallet.
        #
        # Current user is sender
        #     -> show receiver
        #
        # Current user is receiver
        #     -> show sender
        # =====================================================

        if transaction_log.wallet_id == transaction.sender_wallet_id:

            other_wallet = receiver_wallet
            other_user = receiver_user
            other_account = receiver_account

        else:

            other_wallet = sender_wallet
            other_user = sender_user
            other_account = sender_account

        # =====================================================
        # Build other user's wallet information
        # =====================================================

        wallet_info = WalletInfo(
            wallet_id=other_wallet.wallet_id,
            user_id=other_account.account_id,
            phone_no=other_user.phone_no,
            full_name=other_account.full_name,
            account_type=other_user.account_type,
        )

        # =====================================================
        # Build transaction log item
        # =====================================================

        items.append(
            TransactionLogListItem(
                log_id=transaction_log.log_id,
                trx_id=transaction.trx_id,
                trx_type=transaction_log.trx_type,
                amount=transaction.amount,
                status=transaction.status,
                note=transaction.note,
                operation=operation.operation_name,
                user_id=account_id,
                wallet_info=wallet_info,
                created_at=transaction_log.created_at,
            )
        )

    # =========================================================
    # 10. Return paginated result
    # =========================================================

    return PageResult[TransactionLogListItem](
        items=items,
        page=page,
        size=size,
        total=total,
    )