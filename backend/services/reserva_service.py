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

#Mostra as reservas todas de um utilizador (sendo dono e sendo solcitante)
async def lista_reservas_service(db:session, utilizador_id:int):

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
            ConfirmarCaucaoDono = reserva.ConfirmarCaucaoDono
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
            EstadoReserva = reserva.DescEstadoPedidoReserva
        ))

    return lista_reservas_dono, lista_reservas_solicitante

#Mostra os pedidos de reserva todos de um utlizador (sendo dono e sendo solcitante)
async def lista_pedidos_reserva_service(db:session, utilizador_id:int):

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

#Submete a justificação da não entrega da caução e mau estado do produto
async def inserir_justificacao_caucao_service(db:session, reserva_id:int, justificacao:str):
    try:
        mensagem = await reserva_repo.inserir_justificacao_caucao_db(db,reserva_id,justificacao)
        return mensagem
    except Exception as e:
        return {'details: '+ str(e)}

#Indica o bom estado do produto e que a caução será entregue
async def inserir_bom_estado_produto_e_devolucao_caucao(db:session, reserva_id:int):
    try:
        mensagem = await reserva_repo.inserir_bom_estado_produto_e_devolucao_caucao(db,reserva_id)
        return mensagem
    except Exception as e:
        return {'details: '+ str(e)}