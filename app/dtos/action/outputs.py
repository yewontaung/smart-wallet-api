from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from app.data.enums import AIActionStatus
from app.dtos.base import BaseDto


class ActionResult(BaseDto):
    action_result:Any
    action_type:str
    message:str

class AgentHook(BaseDto):
    hook_url:str
    hook_method:str
    form_payload:dict[str, Any] = {}
    require_payload:dict[str, Any] = {}
    require_pin:bool

class AgentAction(BaseDto):
    action_id:UUID
    intent:str
    description:str
    status:AIActionStatus = AIActionStatus.PENDING
    is_error:bool = False
    agent_hook:Optional[AgentHook] = None
    form_display:dict[str, Any] = {}

class AgentResponse(BaseDto):
    message_id:int
    prompt:str
    created_at:datetime
    account_id:int

    agent_actions:list[AgentAction]