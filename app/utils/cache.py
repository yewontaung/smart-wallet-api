from collections import defaultdict
from typing import Any


class InMemoryCache:

    def __init__(self):
        self.storage:dict[str, Any] = defaultdict()

    def store(self, key:str, value:Any):
        self.storage[key] = value
    
    def pop(self, key) -> Any:

        return self.storage.pop(key)