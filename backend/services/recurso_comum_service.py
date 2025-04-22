from requests import Session
import db.repository.recurso_comum_repo as recurso_comum_repo
import db.session as session
from fastapi import HTTPException
from schemas.notificacao_schema import *
from db.repository.notificacao_repo import get_tipo_processo_id
from datetime import date
from db.models import Notificacao, PedidoManutencao
from schemas.recurso_comum_schema import *
from services.notificacao_service import *
from schemas.recurso_comum_schema import *
from schemas.user_schemas import UserJWT

#region Gestão dos Recursos Comuns

#Inserir um novo recurso comum
async def inserir_recurso_comum_service(db:session, recurso_comum:RecursoComumSchemaCreate):

    return await recurso_comum_repo.inserir_recurso_comum_db(db,recurso_comum)


#endregion

#region Pedidos de Novos Recursos Comuns

#Inserir um pedido de um novo recurso comum
async def inserir_pedido_novo_recurso_service(db:session, pedido:PedidoNovoRecursoSchemaCreate):
    try:
        msg, novo_pedido = await recurso_comum_repo.inserir_pedido_novo_recurso_db(db,pedido)

        msg_noti = await cria_notificacao_insercao_pedido_novo_recurso_comum_service(db, novo_pedido) #Criação da notificação

        return msg, msg_noti
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def listar_pedidos_novos_recursos_service(db:session):
    pedidos_novos_recursos = await recurso_comum_repo.listar_pedidos_novos_recursos_db(db)

    if not pedidos_novos_recursos:
        raise HTTPException(status_code=400, detail="Nenhum pedido de novo recurso encontrado")

    return pedidos_novos_recursos

#endregion

#region Pedidos de Manutenção

#Inserir um pedido de manutenção de um recurso comum
async def inserir_pedido_manutencao_service(db:session, pedido:PedidoManutencaoSchemaCreate):

    return await recurso_comum_repo.inserir_pedido_manutencao_db(db,pedido)

#Listar pedidos de manutenção
async def listar_pedidos_manutencao_service(db:session):

    pedidos_manutencao = await recurso_comum_repo.listar_pedidos_manutencao_db(db)

    if not pedidos_manutencao:
        raise HTTPException(status_code=400, detail="Nenhum pedido de manutenção encontrado")

    return pedidos_manutencao

async def obter_all_tipo_estado_pedido_manutencao(db:session):
    try:
        return await recurso_comum_repo.obter_all_tipo_estado_pedido_manutencao(db)
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

async def update_pedido_manutencao(db:Session, u_pedido:PedidoManutencaoUpdateSchema, token:UserJWT):
    try:
        pedido_manutencao = await obter_pedido_manutencao(db, u_pedido.PMID)
        if u_pedido.DescPedido is None:
            return False, "Descrição do Pedido não introduzida"
        elif token.role == "residente" and pedido_manutencao.UtilizadorID != token.id:
            return False, "Utilizador não têm permissão para alterar os dados do pedido de manutenção"
        return await recurso_comum_repo.update_pedido_manutencao_db(db, u_pedido)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Elimina um pedido de manutenção
async def eliminar_pedido_manutencao_service(db:Session, pedido_id:int, token:UserJWT):
    try:
        pedido_manutencao = await obter_pedido_manutencao(db, pedido_id)
        if token.role == "residente" and pedido_manutencao.UtilizadorID != token.id:
            return {'Utilizador não têm permissão para alterar os dados do pedido de manutenção'}
        return await recurso_comum_repo.eliminar_pedido_manutencao(db, pedido_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#endregion

#region Manutenção de Recursos Comuns

async def criar_manutencao_service(db:session, manutencao:ManutencaoCreateSchema):
    try:
        return await recurso_comum_repo.criar_manutencao_db(db,manutencao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def visualizar_manutencoes(db:session):
    manutencoes = await recurso_comum_repo.listar_manutencoes_db(db)

    if not manutencoes:
        raise HTTPException(status_code=400, detail="Nenhuma manutenção encontrada")
    return manutencoes

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

async def obter_manutencao(db:Session, id_manutencao:int):
    try:
        return await recurso_comum_repo.obter_manutencao_db(db, id_manutencao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_manutencao(db:Session, u_pedido:ManutencaoUpdateSchema):
    try:
        if u_pedido.ManutencaoID is None or u_pedido.PMID is None or u_pedido.EntidadeID is None or u_pedido.DataManutencao is None or u_pedido.DescManutencao is None:
            return False, "Erro, um dos campos não foi preenchido"
        a = await recurso_comum_repo.update_manutencao_db(db, u_pedido)
        if a is None:
            return HTTPException(status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def eliminar_manutencao_service(db:Session, id_manutencao:int):
    try:
        return await recurso_comum_repo.eliminar_manutencao_db(db, id_manutencao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#endregion

