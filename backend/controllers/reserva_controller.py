from fastapi import APIRouter, Depends
from db.session import get_db
from sqlalchemy.orm import Session
from schemas.reserva_schema import PedidoReservaSchema
from services.reserva_service import *
from typing import List
from middleware.auth_middleware import role_required
from schemas.user_schemas import UserJWT

router = APIRouter(prefix="/reserva", tags=["Reservas"])

@router.get("/pedidosreserva", response_model=List[PedidoReservaSchema])
async def lista_pedidos_reserva(
    db:Session = Depends(get_db),
    token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar todos os pedidos de reserva
    """
    return await lista_pedidos_reserva_service(db)

@router.get("/pedidosreserva/ativos", response_model=List[PedidoReservaSchema])
async def lista_pedidos_reserva_ativos(
    db:Session = Depends(get_db),
    token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar todos os pedidos de reserva ativos (EstadoID == 1)
    """
    return await lista_pedidos_reserva_ativos_service(db)

@router.get("/pedidosreserva/cancelados", response_model=List[PedidoReservaSchema])
async def lista_pedidos_reserva_cancelados(
    db:Session = Depends(get_db),
    token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar todos os pedidos de reserva cancelados (EstadoID == 2)
    """
    return await lista_pedidos_reserva_cancelados_service(db)