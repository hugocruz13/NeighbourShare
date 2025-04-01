from fastapi import APIRouter, Depends
from backend.db.session import get_db
from sqlalchemy.orm import Session
from backend.schemas.reserva_schema import PedidoReservaSchema
from backend.services.reserva_service import *
from typing import Union, Dict, List
from pydantic import BaseModel

class ResponseModelTuple(BaseModel):
    success: bool
    data: Dict[str, str]

ResponseModel = Union[ResponseModelTuple, List[PedidoReservaSchema]]

router = APIRouter(prefix="/reserva", tags=["Reservas"])

@router.get("/pedidosreserva", response_model=ResponseModel)
def lista_pedidos_reserva(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de reserva
    """
    return lista_pedidos_reserva_service(db)

@router.get("/pedidosreserva/ativos", response_model=ResponseModel)
def lista_pedidos_reserva_ativos(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de reserva ativos (EstadoID == 1)
    """
    return lista_pedidos_reserva_ativos_service(db)

@router.get("/pedidosreserva/cancelados", response_model=ResponseModel)
def lista_pedidos_reserva_cancelados(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de reserva cancelados (EstadoID == 2)
    """
    return lista_pedidos_reserva_cancelados_service(db)