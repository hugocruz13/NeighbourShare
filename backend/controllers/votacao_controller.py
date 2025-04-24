from fastapi import APIRouter, Depends,HTTPException
from requests import Session
from starlette.responses import JSONResponse
from db.session import get_db
from middleware.auth_middleware import role_required
from schemas.votacao_schema import Criar_Votacao, Votar, Votar_id, TipoVotacao, TipoVotacaoPedidoNovoRecurso
from schemas.user_schemas import UserJWT
from services.votacao_service import gerir_votacao_novo_recurso, gerir_votacao_pedido_manutencao, gerir_voto, \
    processar_votacoes_expiradas, gerir_votacoes_orcamentos_pm, processar_votacao, get_orcamentos_pedido_novo_recurso_service

router = APIRouter(tags=['Votação'])

@router.post("/criarvotacao")
async def criar_votacao(votacao: Criar_Votacao, user: UserJWT = Depends(role_required(["gestor","admin"])), db: Session = Depends(get_db)):
    try:
        if votacao.tipo_votacao == TipoVotacao.AQUISICAO:
            success = await gerir_votacao_novo_recurso(db, votacao)
        elif votacao.tipo_votacao == TipoVotacao.MANUTENCAO:
            success = await gerir_votacao_pedido_manutencao(db, votacao)
        else:
            raise HTTPException(status_code=400, detail="Tipo de votação inválido")

        if success:
                return JSONResponse(
                    status_code=201,
                    content={
                        "mensagem": "Votação criada com sucesso",
                        "id_votacao": success.id_votacao,
                        "tipo_votacao": votacao.tipo_votacao,
                        "data_inicio": success.data_inicio.isoformat() if success.data_inicio else None,
                        "data_fim": success.data_fim.isoformat() if success.data_fim else None,
                        "processada": success.processada
                    }
                )

        else:
            raise HTTPException(status_code=500, detail="Erro ao criar votação")

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

@router.post("/votar")
async def votar(votacao:Votar, user: UserJWT = Depends(role_required(["residente","gestor", "admin"])), db: Session = Depends(get_db)):
    try:
        if await gerir_voto(db, Votar_id(voto=votacao.voto, id_votacao=votacao.id_votacao, id_user=user.id)):
            return {"mensagem": "Votacao registado com sucesso"}
        else:
            return {"erro": "Erro ao realizar votacao"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.get("/votacao_orcamento_pm")
async def orcamentos_pm(id:int, user: UserJWT = Depends(role_required(["residente","gestor"])), db: Session = Depends(get_db)):
    try:
        return await gerir_votacoes_orcamentos_pm(db,id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.get("/votacao_orcamento_pedido_novo_recurso")
async def orcamentos_pedido_novo_recurso(votacao_id:int, user: UserJWT = Depends(role_required(["residente","gestor"])), db:Session = Depends(get_db)):
    try:
        return await get_orcamentos_pedido_novo_recurso_service(db,votacao_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.get("/terminar_votacao")
async def testar_processamento_votacao(votacao_id: int,db: Session = Depends(get_db)):
    try:
        return await processar_votacao(db,votacao_id)
    except HTTPException as he:
        raise he