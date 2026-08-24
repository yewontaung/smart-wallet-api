from agentic_runtime.runtime.runtime import Intent, ToolCallingRuntime, ToolRegistry
from agentic_runtime.model.api import HTTPModelApi
from agentic_runtime.mappers import mappers

from app.utils import env

model_api = HTTPModelApi(
    api_key=env.API_KEY,
    api_url=env.API_URL
)

tool_registry = ToolRegistry()

runtime = ToolCallingRuntime(
    api=model_api,
    tool_registry=tool_registry,
    mapper_registry=mappers.registry,
    show_log=True,
)

tool = tool_registry.register

from agentic_runtime.mappers.base import GenericBaseMapper
from agentic_runtime.schemas.intent import ViewBalance

@mappers.registry(Intent.VIEW_BALANCE)
class ViewBalanceMapper(GenericBaseMapper[ViewBalance]):
    ...