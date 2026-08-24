from collections import defaultdict
from typing import Any

from fastapi import WebSocket


class WebSocketConnectionManager:

    def __init__(self):
        self.socket_store:dict[int, WebSocket] = defaultdict()

    async def connect(self, socket_id:int, socket:WebSocket):
        await socket.accept()
        self.socket_store[socket_id] = socket

    def disconnect(self, socket_id:int):
        if socket_id in self.socket_store:
            self.socket_store.pop(socket_id)

    async def broadcast(self, message:str):
        return

    async def send_payload_by_id(self, socket_id:int, payload:dict[str, Any]):
        if socket_id not in self.socket_store:
            return
        socket = self.socket_store[socket_id]
        await socket.send_json(payload)