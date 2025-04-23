from fastapi import APIRouter, Depends,HTTPException
from requests import Session
from db.session import get_db
from middleware.auth_middleware import role_required
from schemas.votacao_schema import Criar_Votacao_Novo_Recurso, Criar_Votacao_Pedido_Manutencao, Votar, Votar_id
from schemas.user_schemas import UserJWT
from services.votacao_service import gerir_votacao_novo_recurso, gerir_votacao_pedido_manutencao, gerir_voto, processar_votacoes_expiradas

router = APIRouter(tags=['Votação'])

@router.post("/criarvotacao_novo_recurso")
async def criar_votacao(votacao: Criar_Votacao_Novo_Recurso, user: UserJWT = Depends(role_required(["gestor"])), db: Session = Depends(get_db)):
    try:
        if await gerir_votacao_novo_recurso(db, votacao):
            return {"mensagem": "Votacao criada com sucesso"}
        else:
            return {"erro": "Erro ao criar votacao"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.post("/criarvotacao_pedido_manutencao")
async def criar_votacao(votacao: Criar_Votacao_Pedido_Manutencao, user: UserJWT = Depends(role_required(["gestor"])), db: Session = Depends(get_db)):
    try:
        if await gerir_votacao_pedido_manutencao(db, votacao):
            return {"mensagem": "Votacao criada com sucesso"}
        else:
            return {"erro": "Erro ao criar votacao"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.post("/votar")
async def votar(votacao:Votar, user: UserJWT = Depends(role_required(["residente","gestor"])), db: Session = Depends(get_db)):
    try:
        if await gerir_voto(db, Votar_id(voto=votacao.voto, id_votacao=votacao.id_votacao, id_user=user.id)):
            return {"mensagem": "Votacao registado com sucesso"}
        else:
            return {"erro": "Erro ao realizar votacao"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

async def testar_processamento_votacao(db: Session = Depends(get_db)):
    return await processar_votacoes_expiradas(db)