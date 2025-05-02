import db.repository.reserva_repo as reserva_repo
import db.session as session
from fastapi import HTTPException
from db.repository.reserva_repo import get_pedido_reserva_db
from schemas.reserva_schema import *
from services import notificacao_service
from services.notificacao_service import *


async def cria_pedido_reserva_service(db:session, pedido_reserva : PedidoReservaSchemaCreate):
    try:
        if pedido_reserva.DataInicio > pedido_reserva.DataFim:
            raise HTTPException(status_code=500, detail='Data de inicio é depois da data de fim')
        else:
            mensagem, pedido_reserva_1 = await reserva_repo.criar_pedido_reserva_db(db,pedido_reserva)
            msg_noti = await cria_notificacao_recebimento_pedido_reserva(db,pedido_reserva_1)
            return mensagem, msg_noti
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Muda o estado de um pedido de reserva
async def muda_estado_pedido_reserva_service(db:session, pedido_reserva_id: int, estado:PedidoReservaEstadosSchema, motivo_recusa:str = None):
    try:
        msg_noti = None
        msg, pedido_reserva =  await reserva_repo.muda_estado_pedido_reserva_db(db,pedido_reserva_id,estado)
        if estado == PedidoReservaEstadosSchema.REJEITADO:
            msg_noti = await cria_notificacao_recusa_pedido_reserva(db,pedido_reserva,motivo_recusa)
        return msg, msg_noti, pedido_reserva
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def cria_reserva_service(db:session, reserva: ReservaSchemaCreate):
    try:
        mensagem = await reserva_repo.cria_reserva_db(db,reserva)
        msg_muda_estado_pedido, msg_noti ,pedido_reserva = await muda_estado_pedido_reserva_service(db,reserva.PedidoReservaID,PedidoReservaEstadosSchema.APROVADO)
        if pedido_reserva.DataInicio == datetime.date.today():
            await muda_recurso_para_indisponivel(db,pedido_reserva.RecursoID)
        msg_noti = await cria_notificacao_aceitacao_pedido_reserva(db,pedido_reserva)

        return mensagem, msg_muda_estado_pedido, msg_noti
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def muda_recurso_para_indisponivel(db:session, recurso_id:int):
    try:
        return await muda_recurso_para_indisponivel(db,recurso_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_reserva_service(db:session, reserva_id:int):
    try:
        return await reserva_repo.get_reserva_db(db,reserva_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Mostra as reservas todas de um utilizador (sendo dono e sendo solcitante)
async def lista_reservas_service(db:session, utilizador_id:int):
    try:
        reservas_dono, reservas_solicitante = await reserva_repo.lista_reservas_db(db, utilizador_id)

        if not reservas_dono and not reservas_solicitante :
            raise HTTPException(status_code=400, detail="Nenhuma reserva encontrada")

        lista_reservas_dono = []
        lista_reservas_solicitante = []

        for reserva in reservas_dono:

            lista_reservas_dono.append(ReservaGetDonoSchema(
                ReservaID = reserva.ReservaID,
                Solicitante = reserva.NomeUtilizador,
                DataInicio = reserva.DataInicio,
                DataFim = reserva.DataFim,
                NomeRecurso = reserva.Nome,
                RecursoEntregueDono = reserva.RecursoEntregueDono,
                ConfirmarCaucaoDono = reserva.ConfirmarCaucaoDono,
                DevolucaoCaucao = reserva.DevolucaoCaucao,
                EstadoRecurso= reserva.EstadoRecurso,
                JustificacaoEstadoProduto= reserva.JustificacaoEstadoProduto
            ))

        for reserva in reservas_solicitante:

            lista_reservas_solicitante.append(ReservaGetSolicitanteSchema(
                ReservaID = reserva.ReservaID,
                Dono= reserva.NomeUtilizador,
                DataInicio = reserva.DataInicio,
                DataFim = reserva.DataFim,
                NomeRecurso = reserva.Nome,
                RecursoEntregueSolicitante = reserva.RecursoEntregueVizinho,
                ConfirmarCaucaoSolicitante = reserva.ConfirmarCaucaoVizinho,
                EstadoReserva = reserva.DescEstadoPedidoReserva,
                DevolucaoCaucao=reserva.DevolucaoCaucao,
                EstadoRecurso=reserva.EstadoRecurso,
                JustificacaoEstadoProduto=reserva.JustificacaoEstadoProduto
            ))

        return lista_reservas_dono, lista_reservas_solicitante
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Mostra os pedidos de reserva todos de um utlizador (sendo dono e sendo solcitante)
async def lista_pedidos_reserva_service(db:session, utilizador_id:int):
    try:
        pedidos_reserva_dono, pedidos_reserva_solicitante = await reserva_repo.lista_pedidos_reserva_db(db, utilizador_id)

        if not pedidos_reserva_dono and not pedidos_reserva_solicitante :
            raise HTTPException(status_code=400, detail="Nenhum pedido de reserva encontrado")

        lista_pedidos_reserva_dono = []
        lista_pedidos_reserva_solicitante = []

        for pedido_reserva in pedidos_reserva_dono:

            lista_pedidos_reserva_dono.append(PedidoReservaGetDonoSchema(
                PedidoReservaID= pedido_reserva.PedidoResevaID,
                RecursoID= pedido_reserva.RecursoID,
                RecursoNome= pedido_reserva.Nome,
                UtilizadorNome= pedido_reserva.NomeUtilizador,
                DataInicio= pedido_reserva.DataInicio,
                DataFim= pedido_reserva.DataFim,
                EstadoPedidoReserva= pedido_reserva.DescEstadoPedidoReserva
            ))

        for pedido_reserva in pedidos_reserva_solicitante:

            lista_pedidos_reserva_solicitante.append(PedidoReservaGetSolicitanteSchema(
                PedidoReservaID= pedido_reserva.PedidoResevaID,
                RecursoID = pedido_reserva.RecursoID,
                RecursoNome = pedido_reserva.Nome,
                NomeDono = pedido_reserva.NomeUtilizador,
                DataInicio = pedido_reserva.DataInicio,
                DataFim= pedido_reserva.DataFim,
                EstadoPedidoReserva = pedido_reserva.DescEstadoPedidoReserva
            ))

        return lista_pedidos_reserva_dono, lista_pedidos_reserva_solicitante
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#Confirma a entrega de um recurso para empréstimo (dono)
async def confirma_entrega_recurso_service(db:session, reserva_id:int):
    try:
        mensagem = await reserva_repo.confirma_entrega_recurso_dono_db(db,reserva_id)
        return mensagem
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Confirma a receção de um recurso numa reserva (pessoa que vai usufrir do recurso)
async def confirma_rececao_recurso_service(db:session, reserva_id:int):
    try:
        mensagem = await reserva_repo.confirma_rececao_recurso_db(db,reserva_id)
        return mensagem
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Confirma a entrega da caução ao dono do produto
async def confirma_entrega_caucao_service(db:session, reserva_id:int):
    try:
        mensagem = await reserva_repo.confirma_entrega_caucao_db(db,reserva_id)
        return mensagem
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Confirma a receção da caução por parte da pessoa que irá usar o produto
async def confirma_rececao_caucao_service(db:session, reserva_id:int):
    try:
        mensagem = await reserva_repo.confirma_rececao_caucao_db(db,reserva_id)
        return mensagem
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Submete a justificação da não entrega da caução e mau estado do produto
async def inserir_justificacao_caucao_service(db:session, reserva_id:int, justificacao:str):
    try:
        mensagem = await reserva_repo.inserir_justificacao_caucao_db(db,reserva_id,justificacao)
        msg_noti = await cria_notificacao_nao_caucao_devolucao_pedido_reserva(db,await get_pedido_reserva_db(db, reserva_id),reserva_id,justificacao)
        return mensagem, msg_noti
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Indica o bom estado do produto e que a caução será entregue
async def inserir_bom_estado_produto_e_devolucao_caucao(db:session, reserva_id:int):
    try:
        mensagem = await reserva_repo.inserir_bom_estado_produto_e_devolucao_caucao_db(db,reserva_id)
        msg_noti = await cria_notificacao_caucao_devolucao_pedido_reserva(db,await get_pedido_reserva_db(db, reserva_id),reserva_id)
        return mensagem, msg_noti
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))