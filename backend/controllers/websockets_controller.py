from fastapi import FastAPI, WebSocket
from typing import Dict

app = FastAPI()
active_connections: Dict[int, WebSocket] = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except RuntimeError:
        del active_connections[user_id]

async def send_notification(user_id: int, message: str):
    if user_id in active_connections:
        await active_connections[user_id].send_text(message)