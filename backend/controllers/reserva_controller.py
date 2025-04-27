from fastapi import APIRouter, Depends, HTTPException, Form
from db.session import get_db
from sqlalchemy.orm import Session
from middleware.auth_middleware import *
from services.reserva_service import *
from typing import List, Tuple
from middleware.auth_middleware import role_required
from schemas.user_schemas import UserJWT

router = APIRouter(prefix="/reserva", tags=["Reservas"])

@router.post("/criar")
async def criar_reserva(
        pedido_reserva_id: int,
        token: UserJWT = Depends(role_required(["admin", "gestor", "residente"])),
        db:Session = Depends(get_db)):
    try:
        reserva = ReservaSchemaCreate(PedidoReservaID=pedido_reserva_id)
        return await cria_reserva_service(db, reserva)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Mostra as reservas todas de um utilizador (sendo dono e sendo solcitante)
@router.get("/lista", response_model=Tuple[List[ReservaGetDonoSchema],List[ReservaGetSolicitanteSchema]])
async def lista_reservas(
        token: UserJWT = Depends(role_required(["admin", "gestor", "residente"])),
        db:Session = Depends(get_db)
):
    try:
        return await lista_reservas_service(db, token.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Confirma a entrega de um recurso para empréstimo (dono)
@router.post("/confirma/entrega/recurso")
async def confirma_entrega_recurso(
        reserva_id: int,
        token: UserJWT = Depends(role_required(["admin", "gestor", "residente"])),
        db:Session = Depends(get_db)
):
    try:
        return await confirma_entrega_recurso_service(db, reserva_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Confirma a receção de um recurso numa reserva (pessoa que vai usufrir do recurso)
@router.post("/confirma/rececao/recurso")
async def confirma_rececao_recurso(
        reserva_id: int,
        token: UserJWT = Depends(role_required(["admin", "gestor", "residente"])),
        db:Session = Depends(get_db)
):
    try:
        return await confirma_rececao_recurso_service(db, reserva_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Confirma a entrega da caução ao dono do produto
@router.post("/confirma/entrega/caucao")
async def confirma_entrega_caucao(
        reserva_id: int,
        token: UserJWT = Depends(role_required(["admin", "gestor", "residente"])),
        db:Session = Depends(get_db)
):
    try:
        return await confirma_entrega_caucao_service(db, reserva_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Confirma a receção da caução por parte da pessoa que irá usar o produto
@router.post("/confirma/rececao/caucao")
async def confirma_rececao_caucao(
        reserva_id: int,
        token: UserJWT = Depends(role_required(["admin", "gestor", "residente"])),
        db:Session = Depends(get_db)
):
    try:
        return await confirma_rececao_caucao_service(db, reserva_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Submissão da justificação do mau estado do produto e não entrega da caução
@router.post("/submissao/justificacao")
async def inserir_justificacao_caucao(
        reserva_id: int,
        justificacao: str,
        token: UserJWT = Depends(role_required(["admin", "gestor", "residente"])),
        db:Session = Depends(get_db)
):
    try:
        return await inserir_justificacao_caucao_service(db, reserva_id, justificacao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Confirmação do bom estado do produto e da devolução da caução
@router.post("/confirma/bomestado")
async def confirma_bom_estado_produto_e_devolucao_caucao(
        reserva_id: int,
        token: UserJWT = Depends(role_required(["admin", "gestor", "residente"])),
        db:Session = Depends(get_db)
):
    try:
        return await inserir_bom_estado_produto_e_devolucao_caucao(db, reserva_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Mostra os pedidos de reserva todos de um utlizador (sendo dono e sendo solcitante)
@router.get("/pedidosreserva/lista", response_model=Tuple[List[PedidoReservaGetDonoSchema],List[PedidoReservaGetSolicitanteSchema]])
async def lista_pedidos_reserva(
    db:Session = Depends(get_db),
    token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))):
    try:
        return await lista_pedidos_reserva_service(db, token.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pedidosreserva/criar")
async def criar_pedido_reserva(
    recurso_id: int = Form(...),
    data_inicio: datetime.date = Form(...),
    data_fim: datetime.date = Form(...),
    db:Session = Depends(get_db),
    token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    try:
        pedido_reserva = PedidoReservaSchemaCreate(
            UtilizadorID = token.id,
            RecursoID = recurso_id,
            DataInicio = data_inicio,
            DataFim = data_fim
        )

        return await cria_pedido_reserva_service(db,pedido_reserva)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pedidosreserva/recusar")
async def recusar_pedido_reserva(
    pedido_reserva_id: int,
    motivo_recusacao: str,
    db:session = Depends(get_db),
    token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    try:
        msg, msg_noti, pedido_reserva = await muda_estado_pedido_reserva_service(db, pedido_reserva_id, PedidoReservaEstadosSchema.REJEITADO, motivo_recusacao)

        return msg, msg_noti
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
