import backend.db.repository.reserva_repo as reserva_repo
import backend.db.session as session
from fastapi import HTTPException

async def lista_pedidos_reserva_service(db:session):

    lista_pedidos = await reserva_repo.lista_pedidos_reserva_db(db)

    if not lista_pedidos:
        raise HTTPException(status_code=400, detail="Nenhum pedido de reserva encontrado")

    return lista_pedidos

async def lista_pedidos_reserva_ativos_service(db: session):
    lista_pedidos_ativos = await reserva_repo.lista_pedidos_reserva_ativos_repo(db)

    if not lista_pedidos_ativos:
        raise HTTPException(status_code=400, detail="Nenhum pedido de reserva ativo encontrado")

    return lista_pedidos_ativos

async def lista_pedidos_reserva_cancelados_service(db:session):

    lista_pedidos_cancelados = await reserva_repo.lista_pedidos_reserva_cancelados_repo(db)

    if not lista_pedidos_cancelados:
        raise HTTPException(status_code=400, detail="Nenhum pedido de reserva cancelado encontrado")

    return lista_pedidos_cancelados




