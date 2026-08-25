
from uuid import uuid4

from sqlmodel import Session, select

from app.data import database
from app.data.models import Wallet
from app.deps import agent, ws
from agentic_runtime.runtime.context import RuntimeContext
from agentic_runtime.schemas.intent import OutOfScope, PayBill, TransferMoney, MobileTopup, ViewBalance

from app.dtos.action.outputs import AgentAction, AgentHook
from app.dtos.base import WebSocketResponse

@agent.tool(TransferMoney)
async def transfer_money_tool(intent:TransferMoney, context:RuntimeContext):
    account_id = context.get_value("account_id", int)
    message_id = context.get_value("message_id", str)

    action = AgentAction(
        message_id=message_id,
        action_id=uuid4(),
        description=f"I think you wanna send {intent.amount} to {intent.receiver}",
        form_display={
            "Receiver": intent.receiver,
            "Amount": intent.amount,
        },
        intent="transfer_money",
        agent_hook=AgentHook(
            form_payload=intent.model_dump(mode="json"),
            hook_method="POST",
            require_pin=False,
            hook_url=f"/ai/handle/transfer_money/{message_id}"
        )
    )

    await ws.connection_manager.send_payload_by_id(account_id, WebSocketResponse(
        message_type="agent_action",
        payload=action,
    ).json_response())

@agent.tool(MobileTopup)
async def mobile_topup_tool(intent:MobileTopup, context:RuntimeContext):
    account_id = context.get_value("account_id", int)
    message_id = context.get_value("message_id", str)

    action = AgentAction(
        message_id=message_id,
        action_id=uuid4(),
        description=f"{intent.phone_number} ကို ဖုန်းဘေ {intent.amount} ဖြည့်ချင်ပါသလား",
        intent="mobile_topup",
        form_display={
            "Phone Number": intent.phone_number, 
            "Phone Bill": intent.amount,
        },
        agent_hook=AgentHook(
            hook_url=f"/ai/handle/mobile_topup/{message_id}",
            form_payload=intent.model_dump(mode="json"),
        )
    )

    await ws.connection_manager.send_payload_by_id(account_id, WebSocketResponse(
        message_type="agent_action",
        payload=action,
    ).json_response())

@agent.tool(PayBill)
@agent.tool(OutOfScope)
async def out_of_scope_tool(intent:OutOfScope | PayBill, context:RuntimeContext):

    account_id:int = context.get_value("account_id", str)
    message_id:int = context.get_value("message_id", str)

    await ws.connection_manager.send_payload_by_id(
        account_id,
        WebSocketResponse(
            message_type="agent_action",
            payload=AgentAction(
                message_id=message_id,
                intent="out_of_scope",
                action_id=uuid4(),
                description=f"Agent is not able to do the task : {intent.__class__.__name__}"
            )
        ).json_response()

    )

@agent.tool(ViewBalance)
async def view_balance_tool(intent:ViewBalance, context:RuntimeContext):
    account_id:int = context.get_value("account_id", str)
    message_id:int = context.get_value("message_id", str)

    with Session(database.engine) as session:
        wallet = session.exec(select(Wallet).where(Wallet.wallet_account_id == account_id)).first()
        database.safe_call(wallet, "Wallet", "wallet_account_id", account_id)
        balance = wallet.current_balance
        phone = wallet.wallet_user.phone_no

    await ws.connection_manager.send_payload_by_id(
        account_id,
        WebSocketResponse(
            message_type="agent_action",
            payload=AgentAction(
                action_id=uuid4(),
                message_id=message_id,
                description="Your Account Balance Info",
                intent="view_balance",
                form_display={
                    "Balance": balance,
                    "Phone": phone,
                }
            )
        ).json_response()
    )
