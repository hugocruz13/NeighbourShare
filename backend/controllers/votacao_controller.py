from fastapi import APIRouter, Depends,HTTPException
from requests import Session
from db.session import get_db
from middleware.auth_middleware import role_required
from schemas.votacao_schema import Criar_Votacao, Pedido_Novo_Recurso
from schemas.user_schemas import UserJWT
from services.votacao_service import gerir_votacao, votacao_nr

router = APIRouter(tags=['Votação'])

@router.post("/criarvotacao")
async def criar_votacao(votacao: Criar_Votacao, user: UserJWT = Depends(role_required(["gestor"])), db: Session = Depends(get_db)):
    try:
        vot =await gerir_votacao(db, votacao)
        return {"id": vot.id, "titulo": vot.titulo, "descricao": vot.descricao, "data_inicio": vot.data_str, "data_fim": vot.data_end}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.post("/criarvotacao_novo_pedido")
async def criar_votacao_novo_pedido(votacao:Pedido_Novo_Recurso,user: UserJWT = Depends(role_required(["gestor"])), db: Session = Depends(get_db)):
    try:
        return await votacao_nr(db, votacao)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})