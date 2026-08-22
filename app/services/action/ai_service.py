from datetime import datetime
from uuid import uuid4

from sqlmodel import Session
from agentic_runtime.runtime.context import RuntimeContext

from app.data.database import safe_call
from app.data.models import WalletUserAccount
from app.deps import agent, ws
from app.dtos.action.outputs import AgentResponse
from app.dtos.base import WebSocketResponse
from app.dtos.wallet_user.inputs import AIMessageForm


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


