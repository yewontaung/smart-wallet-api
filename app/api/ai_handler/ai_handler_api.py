from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import Authentication
from app.dtos.action.outputs import AgentAction, AgentHook


router = APIRouter(prefix="/handle")

@router.post("/transfer_money")
async def handle_transfer_money(auth_user:Authentication, session:Session = Depends(get_session)):
    result = AgentAction(
        action_id=uuid4(),
        description="",
        intent="transfer_money",
        form_display={
            "Receiver": "Mg Mg - 0989898989",
            "amount": 20000,
        },
        agent_hook=AgentHook(
            hook_url="go",
            hook_method="POST",
            require_pin=True,
            form_payload={
                "receiver_wallet_id": 1,
                "sender_wallet_id": 2,
            },
            require_payload={
                "amount": 90000,
                "note": "payment"
            }
        )
    )

    return result