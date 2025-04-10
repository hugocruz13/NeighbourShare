import db.repository.reserva_repo as reserva_repo
import db.session as session
from fastapi import HTTPException
from schemas.reserva_schema import *

async def cria_pedido_reserva_service(db:session, pedido_reserva : PedidoReservaSchemaCreate):
    try:
        if pedido_reserva.DataInicio > pedido_reserva.DataFim:
            raise HTTPException(status_code=500, detail='Data de inicio é depois da data de fim')
        else:
            mensagem = await reserva_repo.criar_pedido_reserva_db(db,pedido_reserva)
            return mensagem
    except Exception as e:
        return {'details: '+ str(e)}

# Mostra os pedidos de reserva efetuados por um utilizador (utilizador_id)
async def lista_pedidos_reserva_service(db:session, utilizador_id:int):

    lista_pedidos = await reserva_repo.lista_pedidos_reserva_db(db, utilizador_id)

    if not lista_pedidos:
        raise HTTPException(status_code=400, detail="Nenhum pedido de reserva encontrado")

    return lista_pedidos

async def lista_pedidos_reserva_ativos_service(db: session):
    lista_pedidos_ativos = await reserva_repo.lista_pedidos_reserva_ativos_db(db)

    if not lista_pedidos_ativos:
        raise HTTPException(status_code=400, detail="Nenhum pedido de reserva ativo encontrado")

    return lista_pedidos_ativos

async def lista_pedidos_reserva_cancelados_service(db:session):

    lista_pedidos_cancelados = await reserva_repo.lista_pedidos_reserva_cancelados_db(db)

    if not lista_pedidos_cancelados:
        raise HTTPException(status_code=400, detail="Nenhum pedido de reserva cancelado encontrado")

    return lista_pedidos_cancelados

async def cria_reserva_service(db:session, reserva: ReservaSchemaCreate):
    try:
        mensagem = await reserva_repo.cria_reserva_db(db,reserva)
        return mensagem
    except Exception as e:
        return {'details: '+ str(e)}

async def get_reserva_service(db:session, reserva_id:int):
    try:
        return await reserva_repo.get_reserva_db(db,reserva_id)
    except Exception as e:
        return {'details: '+ str(e)}

#Mostra as reservas onde o utilizador (utilizador_id) contêm um recurso emprestado consigo
async def lista_reservas_service(db:session, utilizador_id:int):

    lista_reservas = await reserva_repo.lista_reservas_db(db, utilizador_id)

    if not lista_reservas:
        raise HTTPException(status_code=400, detail="Nenhuma reserva encontrada")

    return lista_reservas

#Confirma a entrega de um recurso para empréstimo (dono)
async def confirma_entrega_recurso_service(db:session, reserva_id:int):
    try:
        mensagem = await reserva_repo.confirma_entrega_recurso_dono_db(db,reserva_id)
        return mensagem
    except Exception as e:
        return {'details: '+ str(e)}

#Confirma a receção de um recurso numa reserva (pessoa que vai usufrir do recurso)
async def confirma_rececao_recurso_service(db:session, reserva_id:int):
    try:
        mensagem = await reserva_repo.confirma_rececao_recurso_db(db,reserva_id)
        return mensagem
    except Exception as e:
        return {'details: '+ str(e)}

#Confirma a entrega da caução ao dono do produto
async def confirma_entrega_caucao_service(db:session, reserva_id:int):
    try:
        mensagem = await reserva_repo.confirma_entrega_caucao_db(db,reserva_id)
        return mensagem
    except Exception as e:
        return {'details: '+ str(e)}

#Confirma a receção da caução por parte da pessoa que irá usar o produto
async def confirma_rececao_caucao_service(db:session, reserva_id:int):
    try:
        mensagem = await reserva_repo.confirma_rececao_caucao_db(db,reserva_id)
        return mensagem
    except Exception as e:
        return {'details: '+ str(e)}
