from datetime import datetime
from uuid import uuid4

from sqlmodel import Session

from app.data.database import safe_call
from app.data.enums import AIActionStatus
from app.data.models import WalletUserAccount
from app.dtos.action.outputs import AgentAction, AgentResponse, AgentHook
from app.dtos.wallet_user.inputs import AIMessageForm


async def ask(form:AIMessageForm, account_id:int, session:Session):
    wallet_user = safe_call(session.get(WalletUserAccount, account_id), "WalletUserAccount", "account_id", account_id)

    return AgentResponse(
        account_id=wallet_user.account_id,
        message_id=1,
        created_at=datetime.now(),
        prompt=form.prompt,
        agent_actions=[
            AgentAction(
                action_id=uuid4(),
                intent="transfer_money",
                description=f"Sending 900000 mmk to 0989898989.",
                is_error=False,
                form_display={
                    "receiver": "0989898989",
                    "amount": "900000"
                },
                agent_hook=AgentHook(
                    hook_method="POST",
                    hook_url="/ai/handle/transfer_money",
                    require_pin=False,
                    form_payload={
                        "receiver": "0989898989",
                        "amount": "900000"
                    }
                )
            ),
            AgentAction(
                action_id=uuid4(),
                intent="view_balance",
                description="Sending money",
                require_pin=True,
                status=AIActionStatus.COMPLETED,
                is_error=False,
                form_display={
                    "balance": "1230000000"
                },
            )
        ]
    )