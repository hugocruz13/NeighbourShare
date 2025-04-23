from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter, Depends
from services.web_sockets_service import register_connection, unregister_connection
from schemas.user_schemas import UserJWT
from middleware.auth_middleware import role_required

from starlette.websockets import WebSocketDisconnect #Não sei se é este import para corrigir a missing module na linha 16

router = APIRouter()

@router.websocket("/ws/{user_id}", )
async def websocket_endpoint(websocket: WebSocket, token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))):
    await websocket.accept()
    register_connection(token.id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        unregister_connection(token.id)