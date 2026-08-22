from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.deps.ws import connection_manager

router = APIRouter()

@router.websocket("/{account_id}")
async def global_socket_endpoint(websocket:WebSocket, account_id:int):
    await connection_manager.connect(account_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"WS Info #Socket {account_id} - data: {data}")
    except WebSocketDisconnect:
        connection_manager.disconnect(account_id)
        print(f"WS #Sockent {account_id} is disconnected.")
