
from uuid import uuid4

from app.deps import agent, ws
from agentic_runtime.runtime.context import RuntimeContext
from agentic_runtime.schemas.intent import TransferMoney, MobileTopup

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
            hook_url="/ai/handle/mobile_topup",
            form_payload=intent.model_dump(mode="json"),
        )
    )

    await ws.connection_manager.send_payload_by_id(account_id, WebSocketResponse(
        message_type="agent_action",
        payload=action,
    ).json_response())
