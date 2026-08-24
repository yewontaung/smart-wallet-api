from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlmodel import Session, select
from agentic_runtime.runtime.context import RuntimeContext

from app.data.database import safe_call
from app.data.models import Wallet, WalletUserAccount
from app.deps import agent, ws
from app.dtos.action.outputs import AgentResponse
from app.dtos.ai.inputs import TransferMoneyRequest
from app.dtos.base import WebSocketResponse
from app.dtos.shared.searches import ReceiverSearch
from app.dtos.wallet_user.inputs import AIMessageForm
from app.services import account_service
from app.utils.resolvers.amount import resolve_burmese_amount
from app.utils.resolvers.phone import is_phone_number, normalize_to_ascii_digits


async def ask(form:AIMessageForm, account_id:int, session:Session):
    wallet_user = safe_call(session.get(WalletUserAccount, account_id), "WalletUserAccount", "account_id", account_id)
    context = RuntimeContext()
    context.add_provider("account_id", wallet_user.account_id)
    context.add_provider("prompt", form.prompt)
    response = AgentResponse(
            message_id=uuid4(),
            account_id=account_id,
            created_at=datetime.now(),
            prompt=form.prompt,
            agent_actions=[]
        )
    context.add_provider("message_id", response.message_id)

    await ws.connection_manager.send_payload_by_id(account_id, WebSocketResponse(
        message_type="ai_response",
        payload=response,
    ).json_response())

    await agent.runtime.prompt(form.prompt, context)

    return {"status": "processing", "message_id": response.message_id}


def resolve_send_money_form(form:TransferMoneyRequest, account_id:int, session:Session) -> dict[str, Any]:
    payload = {}
    amount = resolve_burmese_amount(form.amount)
    payload["amount"] = amount

    sender_wallet = session.exec(select(Wallet).where(Wallet.wallet_account_id == account_id)).first()
    safe_call(sender_wallet, "Wallet", "wallet_account_id", account_id)
    payload["sender_wallet_id"] = sender_wallet.wallet_id

    if is_phone_number(form.receiver):
        phone_number = normalize_to_ascii_digits(form.receiver)
        profile = account_service.search_receiver(ReceiverSearch(phone_no=phone_number), account_id=account_id, session=session)
        payload["receiver"] = f"{profile.full_name} - {profile.phone_no}"
        payload["receiver_wallet_id"] = profile.wallet_id

    return payload