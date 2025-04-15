import db.repository.recurso_comum_repo as recurso_comum_repo
import db.session as session
from fastapi import HTTPException
from schemas.notificacao_schema import *
from db.repository.notificacao_repo import get_tipo_processo_id
from datetime import date
from db.models import Notificacao
from schemas.recurso_comum_schema import *
from services.notificacao_service import *


#Inserir um novo recurso comum
async def inserir_recurso_comum_service(db:session, recurso_comum:RecursoComumSchemaCreate):

    return await recurso_comum_repo.inserir_recurso_comum_db(db,recurso_comum)

#Inserir um pedido de aquisição de um novo recurso comum
async def inserir_pedido_novo_recurso_service(db:session, pedido:PedidoNovoRecursoSchemaCreate):
    try:
        msg, novo_pedido = await recurso_comum_repo.inserir_pedido_novo_recurso_db(db,pedido)

        msg_noti = await cria_notificacao_insercao_pedido_novo_recurso_comum_service(db, novo_pedido) #Criação da notificação

        return msg, msg_noti
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Inserir um pedido de manutenção de um recurso comum
async def inserir_pedido_manutencao_service(db:session, pedido:PedidoManutencaoSchemaCreate):
    try:

        msg, novo_pedido = await recurso_comum_repo.inserir_pedido_manutencao_db(db,pedido)

        msg_noti = await cria_notificacao_insercao_pedido_manutencao_service(db, novo_pedido) #Criação da notificação

        return msg, msg_noti

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def listar_pedidos_novos_recursos_service(db:session):

    pedidos_novos_recursos = await recurso_comum_repo.listar_pedidos_novos_recursos_db(db)

    if not pedidos_novos_recursos:
        raise HTTPException(status_code=400, detail="Nenhum pedido de novo recurso encontrado")

    return pedidos_novos_recursos

async def listar_pedidos_novos_recursos_pendentes_service(db:session):

    pedidos_novos_recursos_pendentes = await recurso_comum_repo.listar_pedidos_novos_recursos_pendentes_db(db)

    if not pedidos_novos_recursos_pendentes:
        raise HTTPException(status_code=400, detail="Nenhum pedido de novo recurso pendente encontrado")

    return pedidos_novos_recursos_pendentes

async def listar_pedidos_novos_recursos_aprovados_service(db:session):

    pedidos_novos_recursos_aprovados = await recurso_comum_repo.listar_pedidos_novos_recursos_aprovados_db(db)

    if not pedidos_novos_recursos_aprovados:
        raise HTTPException(status_code=400, detail="Nenhum pedido de novo recurso aprovado encontrado")

    return pedidos_novos_recursos_aprovados

async def listar_pedidos_manutencao_service(db:session):

    pedidos_manutencao = await recurso_comum_repo.listar_pedidos_manutencao_db(db)

    if not pedidos_manutencao:
        raise HTTPException(status_code=400, detail="Nenhum pedido de manutenção encontrado")

    return pedidos_manutencao

async def listar_pedidos_manutencao_em_progresso_service(db:session):

    pedidos_manutencao_em_progresso = await recurso_comum_repo.listar_pedidos_manutencao_em_progresso_db(db)

    if not pedidos_manutencao_em_progresso:
        raise HTTPException(status_code=400, detail="Nenhum pedido de manutenção em progresso encontrado")

    return pedidos_manutencao_em_progresso

async def listar_pedidos_manutencao_finalizados_service(db:session):

    pedidos_manutencao_finalizados = await recurso_comum_repo.listar_pedidos_manutencao_finalizados_db(db)

    if not pedidos_manutencao_finalizados:
        raise HTTPException(status_code=400, detail="Nenhum pedido de manutenção finalizado encontrado")

    return pedidos_manutencao_finalizados