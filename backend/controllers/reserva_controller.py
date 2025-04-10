from fastapi import APIRouter, Depends, HTTPException
from db.session import get_db
from sqlalchemy.orm import Session
from middleware.auth_middleware import *
from services.reserva_service import *
from typing import List

router = APIRouter(prefix="/reserva", tags=["Reservas"])

@router.post("/criar")
async def criar_reserva(
        pedido_reserva_id: int,
        db:Session = Depends(get_db)
):
    try:

        reserva = ReservaSchemaCreate(PedidoReservaID=pedido_reserva_id)

        return cria_reserva_service(db, reserva)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lista")
async def lista_reservas(
        token: UserJWT = Depends(jwt_middleware),
        db:Session = Depends(get_db)
):
    return await lista_reservas_service(db, token.id)

#Confirma a entrega de um recurso para empréstimo (dono)
@router.post("/confirma/entrega/recurso")
async def confirma_entrega_recurso(
        reserva_id: int,
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
        db:Session = Depends(get_db)
):
    try:
        return await confirma_rececao_caucao_service(db, reserva_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pedidosreserva", response_model=List[PedidoReservaSchema])
async def lista_pedidos_reserva(
    token: UserJWT = Depends(jwt_middleware),
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de reserva efetuados pelo utilizador
    """
    return await lista_pedidos_reserva_service(db, token.id)

@router.get("/pedidosreserva/ativos", response_model=List[PedidoReservaSchema])
async def lista_pedidos_reserva_ativos(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de reserva ativos (EstadoID == 1)
    """
    return await lista_pedidos_reserva_ativos_service(db)

@router.get("/pedidosreserva/cancelados", response_model=List[PedidoReservaSchema])
async def lista_pedidos_reserva_cancelados(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de reserva cancelados (EstadoID == 2)
    """
    return await lista_pedidos_reserva_cancelados_service(db)

@router.post("/pedidosreserva/criar")
async def criar_pedido_reserva(
    recurso_id: int,
    data_inicio: datetime.date,
    data_fim: datetime.date,
    db:Session = Depends(get_db),
    token: UserJWT = Depends(jwt_middleware),
):
    try:
        pedido_reserva = PedidoReservaSchemaCreate(
            UtilizadorID = token.id,
            RecursoID = recurso_id,
            DataInicio = data_inicio,
            DataFim = data_fim
        )

        return cria_pedido_reserva_service(db,pedido_reserva)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

