
from sqlalchemy.orm import joinedload
from backend.db import session
from backend.db.models import PedidoReserva
from sqlalchemy.exc import SQLAlchemyError

async def lista_pedidos_reserva_db(db:session):
    try:
        pedidos_reserva = (
            db.query(PedidoReserva)
            .options(
                joinedload(PedidoReserva.Recurso_),
                joinedload(PedidoReserva.Utilizador_),
                joinedload(PedidoReserva.EstadoPedidoReserva_)
            )
            .all()
        )
        return pedidos_reserva, {'Consulta efetuada com sucesso!'}
    except SQLAlchemyError as e:
        return False, {'details': str(e)}

async def lista_pedidos_reserva_ativos_repo(db:session):
    try:
        pedidos_reserva_ativos = (
            db.query(PedidoReserva)
            .options(
                joinedload(PedidoReserva.Recurso_),
                joinedload(PedidoReserva.Utilizador_),
                joinedload(PedidoReserva.EstadoPedidoReserva_)
            )
            .filter(PedidoReserva.EstadoID == 1)
        )
        return pedidos_reserva_ativos, {'Consulta efetuada com sucesso!'}
    except SQLAlchemyError as e:
        return False, {'details': str(e)}

async def lista_pedidos_reserva_cancelados_repo(db:session):
    try:
        pedidos_reserva_cancelados = (
            db.query(PedidoReserva)
            .options(
                joinedload(PedidoReserva.Recurso_),
                joinedload(PedidoReserva.Utilizador_),
                joinedload(PedidoReserva.EstadoPedidoReserva_)
            )
            .filter(PedidoReserva.EstadoID == 2)
        )
        return pedidos_reserva_cancelados, {'Consulta efetuada com sucesso!'}
    except SQLAlchemyError as e:
        return False, {'details': str(e)}