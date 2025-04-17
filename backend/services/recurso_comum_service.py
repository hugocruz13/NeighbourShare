import db.repository.recurso_comum_repo as recurso_comum_repo
import db.session as session
from fastapi import HTTPException
from schemas.recurso_comum_schema import *
<<<<<<< HEAD
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
=======

#Inserir um novo recurso comum
async def inserir_recurso_comum_service(db:session, recurso_comum:RecursoComumSchemaCreate):
    return await recurso_comum_repo.inserir_recurso_comum_db(db,recurso_comum)

#Inserir um pedido de um novo recurso comum
async def inserir_pedido_novo_recurso_service(db:session, pedido:PedidoNovoRecursoSchemaCreate):
    return await recurso_comum_repo.inserir_pedido_novo_recurso_db(db,pedido)

#Inserir um pedido de manutenção de um recurso comum
async def inserir_pedido_manutencao_service(db:session, pedido:PedidoManutencaoSchemaCreate):
    return await recurso_comum_repo.inserir_pedido_manutencao_db(db,pedido)
>>>>>>> origin/votação

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

async def visualizar_manutencoes(db:session):
    manutencoes = await recurso_comum_repo.listar_manutencoes(db)

    if not manutencoes:
        raise HTTPException(status_code=400, detail="Nenhuma manutenção encontrada")
    return manutencoes

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
            # if tipo_estado_manutencao == 2: #Estado -> Concluída

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
                if e.EstadoPedManuID == 2:  # Estado -> Aprovado para manutenção interna
                    await cria_notificacao_nao_necessidade_entidade_externa(db,await obter_pedido_manutencao(db,id_pedido_manutencao))
                elif e.EstadoPedManuID == 3: # Estado -> Em negociação com entidades externas
                    await cria_notificacao_necessidade_entidade_externa(db,await obter_pedido_manutencao(db,id_pedido_manutencao))
                elif e.EstadoPedManuID == 5: # Estado -> Rejeitado
                    await cria_notificacao_rejeicao_manutencao_recurso_comum(db,await obter_pedido_manutencao(db,id_pedido_manutencao))
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

async def update_pedido_manutencao(db:Session, u_pedido:PedidoManutencaoUpdateSchema):
    try:
        if u_pedido.DataPedido is None or u_pedido.DescPedido is None or u_pedido.PMID is None or u_pedido.RecursoComun_ is None:
            return False, "Erro, um dos campos não foi preenchido"
        return await recurso_comum_repo.update_pedido_manutencao_db(db, u_pedido)
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