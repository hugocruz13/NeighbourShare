from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from backend.db.session import get_db
from backend.models.models import PedidoReserva
from backend.schemas.reserva_schema import PedidoReservaSchema

router = APIRouter(prefix="/reserva", tags=["Reservas"])

@router.get("/pedidosreserva", response_model=List[PedidoReservaSchema])
def lista_pedidos_reserva(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de reserva
    """
    pedidos_reserva = (
        db.query(PedidoReserva)
        .options(
            joinedload(PedidoReserva.Recurso_),
            joinedload(PedidoReserva.Utilizador_),
            joinedload(PedidoReserva.EstadoPedidoReserva_)
        )
        .all()
    )

    if not pedidos_reserva:
        raise HTTPException(status_code=404, detail="Nenhum pedido de reserva encontrado")

    return pedidos_reserva

@router.get("/pedidosreserva/ativos", response_model=List[PedidoReservaSchema])
def lista_pedidos_reserva_ativos(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de reserva ativos (EstadoID == 1)
    """
    pedidos_reserva_ativos = (
        db.query(PedidoReserva)
        .options(
            joinedload(PedidoReserva.Recurso_),
            joinedload(PedidoReserva.Utilizador_),
            joinedload(PedidoReserva.EstadoPedidoReserva_)
        )
        .filter(PedidoReserva.EstadoID == 1)
        .all()
    )

    if not pedidos_reserva_ativos:
        raise HTTPException(status_code=404, detail="Nenhum pedido de reserva encontrado")

    return pedidos_reserva_ativos

@router.get("/pedidosreserva/cancelados", response_model=List[PedidoReservaSchema])
def lista_pedidos_reserva_cancelados(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de reserva cancelados (EstadoID == 2)
    """
    pedidos_reserva_cancelados = (
        db.query(PedidoReserva)
        .options(
            joinedload(PedidoReserva.Recurso_),
            joinedload(PedidoReserva.Utilizador_),
            joinedload(PedidoReserva.EstadoPedidoReserva_)
        )
        .filter(PedidoReserva.EstadoID == 2)
        .all()
    )

    if not pedidos_reserva_cancelados:
        raise HTTPException(status_code=404, detail="Nenhum pedido de reserva encontrado")

    return pedidos_reserva_cancelados