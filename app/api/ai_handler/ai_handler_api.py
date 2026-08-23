from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, Body, Depends, Request
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import Authentication
from app.dtos.action.outputs import AgentAction, AgentHook
from app.dtos.ai.inputs import TransferMoneyRequest
from app.services.action import ai_service


router = APIRouter(prefix="/handle")

@router.post("/transfer_money/{message_id}")
async def handle_transfer_money(
    message_id:UUID, 
    auth_user:Authentication, 
    form:TransferMoneyRequest,
    session:Session = Depends(get_session)):

    print("===========================")
    print(form)
    print("===========================")
    resolved = ai_service.resolve_send_money_form(form, auth_user.user_id, session)

    result = AgentAction(
        message_id=message_id,
        action_id=uuid4(),
        description="",
        intent="transfer_money",
        form_display={
            "Receiver": f"{resolved.get("receiver")}",
            "Amount": f"{resolved.get("amount")}",
        },
        agent_hook=AgentHook(
            hook_url="/wallet-user/action/transfer",
            hook_method="POST",
            require_pin=True,
            form_payload={
                "receiver_wallet_id": resolved.get("receiver_wallet_id"),
                "sender_wallet_id": resolved.get("sender_wallet_id"),
            },
            require_payload={
                "amount": resolved.get("amount"),
                "note": ""
            }
        )
    )

    return result