from fastapi import APIRouter, Depends,HTTPException
from requests import Session
from db.session import get_db
from middleware.auth_middleware import role_required
from schemas.votacao_schema import Criar_Votacao
from schemas.user_schemas import UserJWT
from services.votacao_service import gerir_votacao

router = APIRouter(tags=['Votação'])

@router.post("/criarvotacao_novo_recurso")
async def criar_votacao(votacao: Criar_Votacao, user: UserJWT = Depends(role_required(["gestor"])), db: Session = Depends(get_db)):
    try:
        if await gerir_votacao(db, votacao):
            return {"mensagem": "Votacao criada com sucesso"}
        else:
            return {"erro": "Erro ao criar votacao"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
