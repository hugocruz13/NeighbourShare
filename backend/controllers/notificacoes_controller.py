from fastapi import APIRouter, Depends
from db.session import get_db
from schemas.notificacao_schema import NotificacaoSchema
from schemas.user_schemas import UserJWT
from services.notificacao_service import *
from typing import List
from middleware.auth_middleware import role_required

router = APIRouter(prefix='/notificacoes', tags=['Notificacoes'])

@router.get('/', response_model=List[NotificacaoSchema])
async def listar_notificacoes(db:Session = Depends(get_db), token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))):
    return await listar_notificacoes_service(db, token.id)