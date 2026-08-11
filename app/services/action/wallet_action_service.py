from typing import Optional

from sqlmodel import Session, col, select

from app.data.database import safe_call
from app.data.enums import TransactionStatus, TransactionType
from app.data.models import BusinessProfile, Transaction, TransactionLog, Wallet, WalletOperation
from app.dtos.action.inputs import MobileTopUpForm, PayBillForm, SendMoneyForm
from app.dtos.action.outputs import ActionResult
from app.utils.exceptions import BusinessException, InsufficientBalanceException, InvalidAmountException, UnauthorizedWalletException


def transfer_money(
        sender_wallet:Wallet, 
        receiver_wallet:Wallet,
        amount:float,
        note:Optional[str],
        operation:WalletOperation,
        session:Session
) -> Transaction:
    # get sender balance
    sender_current_balance = sender_wallet.current_balance
    # check balance
    if sender_current_balance < amount:
        raise InsufficientBalanceException()

    # get current balance
    receiver_current_balance = receiver_wallet.current_balance

    # update sender last balance
    sender_wallet.last_balance = sender_current_balance
    # update sender current balance
    sender_wallet.current_balance = sender_current_balance - amount

    # update receiver last balance
    receiver_wallet.last_balance = receiver_current_balance
    # update receiver current balance
    receiver_wallet.current_balance = receiver_current_balance + amount

    # update versions
    sender_wallet.version += 1
    receiver_wallet.version += 1

    # create transaction
    trx = Transaction(
        sender_wallet_id=sender_wallet.wallet_id,
        receiver_wallet_id=receiver_wallet.wallet_id,
        note=note,
        amount=amount,
        status=TransactionStatus.COMPLETED,
        operation_id=operation.operation_id,
    )

    # create transaction logs
    trx_out_log = TransactionLog(
        wallet_id=sender_wallet.wallet_id,
        trx_type=TransactionType.OUT
    )

    trx_in_log = TransactionLog(
        wallet_id=receiver_wallet.wallet_id,
        trx_type=TransactionType.IN
    )

    trx.trx_logs.append(trx_out_log)
    trx.trx_logs.append(trx_in_log)

    return trx



def send_money(form:SendMoneyForm, user_id:int, session:Session) -> ActionResult:

    if form.sender_wallet_id == form.receiver_wallet_id:
        raise BusinessException("Invalid wallet.")

    # locak wallets
    wallets = {
        wallet.wallet_id: wallet
        for wallet in session.exec(
            select(Wallet).where(
                col(Wallet.wallet_id).in_(form.sorted_wallet())
            ).order_by(Wallet.wallet_id)
            .with_for_update()
        ).all()
    }

    # get sender wallet
    sender_wallet = safe_call(
        wallets.get(form.sender_wallet_id), 
        "Wallet", 
        "wallet_id", 
        form.sender_wallet_id)
    # get receiver wallet
    receiver_wallet = safe_call(
        wallets.get(form.receiver_wallet_id), 
        "Wallet", 
        "wallet_id", 
        form.receiver_wallet_id)

    # validation
    if sender_wallet.wallet_account_id != user_id:
        raise UnauthorizedWalletException("Unauthorized wallet user.")

    if form.amount <= 0:
        raise InvalidAmountException("Invalid amount to transfer.")

    operation = safe_call(session.exec(select(WalletOperation).where(WalletOperation.operation_name == "Wallet Transfer")).first(), "WalletOperation", "operation_name", "Wallet Transfer")

    trx = transfer_money(
        sender_wallet=sender_wallet,
        receiver_wallet=receiver_wallet,
        amount=form.amount,
        note=form.note,
        operation=operation,
        session=session,
    )

    # add trx info to session
    session.add(trx)

    # commit db
    session.commit()

    return ActionResult(
        action_result=trx.trx_id,
        action_type="send_money", 
        message=f"{form.amount} is sent from {sender_wallet.wallet_user.phone_no} to {receiver_wallet.wallet_user.phone_no}")

def pay_bill(form:PayBillForm, user_id:int, session:Session) -> ActionResult:
    if form.sender_wallet_id == form.receiver_wallet_id:
        raise BusinessException("Invalid wallet.")

    business = safe_call(session.get(BusinessProfile, form.business_id), "BusinessProfile", "business_id", form.business_id)

    # locak wallets
    wallets = {
        wallet.wallet_id: wallet
        for wallet in session.exec(
            select(Wallet).where(
                col(Wallet.wallet_id).in_(form.sorted_wallet())
            ).order_by(Wallet.wallet_id)
            .with_for_update()
        ).all()
    }

    # get sender wallet
    sender_wallet = safe_call(
        wallets.get(form.sender_wallet_id), 
        "Wallet", 
        "wallet_id", 
        form.sender_wallet_id)
    # get receiver wallet
    receiver_wallet = safe_call(
        wallets.get(form.receiver_wallet_id), 
        "Wallet", 
        "wallet_id", 
        form.receiver_wallet_id)

    if receiver_wallet.wallet_account_id != business.owner_id:
        raise BusinessException("Invalid receiver wallet.")

    # validation
    if sender_wallet.wallet_account_id != user_id:
        raise UnauthorizedWalletException("Unauthorized wallet user.")

    if form.amount <= 0:
        raise InvalidAmountException("Invalid amount to transfer.")

    operation = safe_call(session.exec(select(WalletOperation).where(WalletOperation.operation_name == "Business Payment")).first(), "WalletOperation", "operation_name", "Business Payment")

    trx = transfer_money(
        sender_wallet=sender_wallet,
        receiver_wallet=receiver_wallet,
        amount=form.amount,
        operation=operation,
        note=f"Payment to {business.qualified_name}",
        session=session,
    )

    session.add(trx)
    
    session.commit()

    return ActionResult(
        action_result=trx.trx_id,
        action_type="send_money", 
        message=f"{form.amount} is paid to {business.qualified_name}")

def top_up(form:MobileTopUpForm, auth_user:int, session:Session) -> ActionResult:
    return