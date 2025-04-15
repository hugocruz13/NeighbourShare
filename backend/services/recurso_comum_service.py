from requests import Session

import db.repository.recurso_comum_repo as recurso_comum_repo
import db.session as session
from fastapi import HTTPException

from db.models import PedidoManutencao
from schemas.recurso_comum_schema import *

#Inserir um novo recurso comum
async def inserir_recurso_comum_service(db:session, recurso_comum:RecursoComumSchemaCreate):

    return await recurso_comum_repo.inserir_recurso_comum_db(db,recurso_comum)

#Inserir um pedido de um novo recurso comum
async def inserir_pedido_novo_recurso_service(db:session, pedido:PedidoNovoRecursoSchemaCreate):

    return await recurso_comum_repo.inserir_pedido_novo_recurso_db(db,pedido)

#Inserir um pedido de manutenção de um recurso comum
async def inserir_pedido_manutencao_service(db:session, pedido:PedidoManutencaoSchemaCreate):

    return await recurso_comum_repo.inserir_pedido_manutencao_db(db,pedido)

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

async def obter_all_tipo_estado_pedido_manutencao(db:session):
    try:
        return await recurso_comum_repo.obter_all_tipo_estado_pedido_manutencao(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def obter_all_tipo_estado_manutencao(db:session):
    try:
        return await recurso_comum_repo.obter_all_tipo_estado_manutencao(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def alterar_tipo_estado_manutencao(db:session, id_manutencao:int, tipo_estado_manutencao:int):
    try:
        estados = await obter_all_tipo_estado_manutencao(db)
        if estados is None:
            raise HTTPException(status_code=500, detail="Erro ao obter tipos de estado manutenção")
        if tipo_estado_manutencao in estados:
            await recurso_comum_repo.alterar_estado_manutencao(db, id_manutencao, tipo_estado_manutencao)
            return True
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def alterar_tipo_estado_pedido_manutencao(db:session, id_pedido_manutencao:int, tipo_estado_pedido_manutencao:int):
    try:
        estados = await obter_all_tipo_estado_pedido_manutencao(db)
        if estados is None:
            raise HTTPException(status_code=500, detail="Erro ao obter tipos de estado de pedido manutenção")
        for e in estados:
            if e.EstadoPedManuID == tipo_estado_pedido_manutencao:
                await recurso_comum_repo.alterar_estado_pedido_manutencao(db, id_pedido_manutencao, tipo_estado_pedido_manutencao)
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def obter_pedido_manutencao(db:Session, id_manutencao:int):
    try:
        return await recurso_comum_repo.obter_pedido_manutencao_db(db, id_manutencao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def obter_manutencao(db:Session, id_manutencao:int):
    try:
        return await recurso_comum_repo.obter_manutencao_db(db, id_manutencao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))