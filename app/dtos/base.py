import math
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, computed_field
from pydantic.alias_generators import to_camel

class BaseDto(BaseModel):

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


T = TypeVar("T")
class PageResult(BaseDto, Generic[T]):
    items:list[T]
    page:int
    size:int

    total:int

    @computed_field
    @property
    def pages(self) -> int:
        return math.ceil(self.total / self.size)

class ModificationResult(BaseDto):
    result_item:Any
    is_success:bool
    message:Optional[str] = None
