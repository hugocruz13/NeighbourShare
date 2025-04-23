from typing import Dict
from fastapi import WebSocket

# Mapa global de conexões
active_connections: Dict[int, WebSocket] = {}

def register_connection(user_id: int, websocket: WebSocket):
    active_connections[user_id] = websocket

def unregister_connection(user_id: int):
    active_connections.pop(user_id, None)

async def send_notification(user_id: int, notificacao_obj: dict):
    websocket = active_connections.get(user_id)
    if websocket:
        await websocket.send_json(notificacao_obj)