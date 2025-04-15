from sqlalchemy.orm import joinedload, aliased
from db import session
from db.models import PedidoReserva, Reserva, Recurso, Utilizador, EstadoPedidoReserva
from schemas.reserva_schema import *
from sqlalchemy.exc import SQLAlchemyError

async def criar_pedido_reserva_db(db:session, pedido_reserva : PedidoReservaSchemaCreate):

    try:
        novo_pedido_reserva = PedidoReserva(
            UtilizadorID= pedido_reserva.UtilizadorID,
            RecursoID= pedido_reserva.RecursoID,
            DataInicio= pedido_reserva.DataInicio,
            DataFim= pedido_reserva.DataFim,
            EstadoID=1 #Estado do pedido de reserva -> Em análise (ID : 1)
        )

        db.add(novo_pedido_reserva)
        db.commit()
        db.refresh(novo_pedido_reserva)

        return {'Pedido de reserva criado com sucesso!'}, pedido_reserva
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

async def lista_pedidos_reserva_ativos_db(db:session):
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
        return pedidos_reserva_ativos
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def lista_pedidos_reserva_cancelados_db(db:session):
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
        return pedidos_reserva_cancelados
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

# Muda o estado de um pedido de reserva
async def muda_estado_pedido_reserva_db(db:session, pedido_reserva_id:int, estado:PedidoReservaEstadosSchema):
    try:
        estado_id = db.query(EstadoPedidoReserva).filter(EstadoPedidoReserva.DescEstadoPedidoReserva == estado.value).first().EstadoID

        if not estado_id:
            return {'Estado de pedido de reserva não encontrado!'}

        pedido_reserva = db.query(PedidoReserva).filter(PedidoReserva.PedidoResevaID == pedido_reserva_id).first()
        pedido_reserva.EstadoID = estado_id
        db.commit()

        return {'Estado do pedido de reserva alterado com sucesso!'}, pedido_reserva
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def cria_reserva_db(db:session, reserva:ReservaSchemaCreate):
    try:
        nova_reserva = Reserva(
            PedidoResevaID=reserva.PedidoReservaID,
            ConfirmarCaucaoDono= False,
            ConfirmarCaucaoVizinho= False,
            RecursoEntregueDono= False,
            RecursoEntregueVizinho= False,
            DevolucaoCaucao= False,
            EstadoRecurso= False
        )

        db.add(nova_reserva)
        db.commit()
        db.refresh(nova_reserva)

        return {'Reserva criada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

#Obtem os dados de uma reserva através do seu ID
async def get_reserva_db(db:session, reserva_id: int):
    try:
        reserva = db.query(Reserva).filter(Reserva.ReservaID == reserva_id).first()
        return reserva
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

#Obtêm um pedido de reserva através do seu ID
async def get_pedido_reserva_db(db:session, pedido_reserva_id: int):
    try:
        pedido_reserva = db.query(PedidoReserva).filter(PedidoReserva.PedidoResevaID == pedido_reserva_id).first()
        return pedido_reserva
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

# Mostra as reservas todas de um utilizador (sendo dono e sendo solcitante)
async def lista_reservas_db(db:session, utilizador_id: int):
    try:

        utilizador_pedido = aliased(Utilizador)

        reservas_dono = db.query(
        Reserva.ReservaID,
        utilizador_pedido.NomeUtilizador,
        PedidoReserva.DataInicio,
        PedidoReserva.DataFim,
        Recurso.Nome,
        Reserva.RecursoEntregueDono,
        Reserva.ConfirmarCaucaoDono
        ).join(
            PedidoReserva, PedidoReserva.PedidoResevaID == Reserva.PedidoResevaID
        ).join(
            Recurso, Recurso.RecursoID == PedidoReserva.RecursoID
        ).join(
            Utilizador, Utilizador.UtilizadorID == Recurso.UtilizadorID
        ).join(
            utilizador_pedido, utilizador_pedido.UtilizadorID == PedidoReserva.UtilizadorID
        ).filter(
            Utilizador.UtilizadorID == utilizador_id
        ).all()

        reservas_solicitante = (db.query(
            Reserva.ReservaID,
            Utilizador.NomeUtilizador,
            PedidoReserva.DataInicio,
            PedidoReserva.DataFim,
            Recurso.Nome,
            Reserva.RecursoEntregueVizinho,
            Reserva.ConfirmarCaucaoVizinho,
            EstadoPedidoReserva.DescEstadoPedidoReserva
        ).join(
            PedidoReserva, PedidoReserva.PedidoResevaID == Reserva.PedidoResevaID
        ).join(
            Recurso, Recurso.RecursoID == PedidoReserva.RecursoID
        ).join(
            Utilizador, Utilizador.UtilizadorID == PedidoReserva.UtilizadorID
        ).join(
            EstadoPedidoReserva, EstadoPedidoReserva.EstadoID == PedidoReserva.EstadoID
        ).filter(
            PedidoReserva.UtilizadorID == utilizador_id
        ).all())

        return reservas_dono, reservas_solicitante

    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

#Mostra os pedidos de reserva todos de um utlizador (sendo dono e sendo solcitante)
async def lista_pedidos_reserva_db(db:session, utilizador_id: int):
    try:
        pedidos_reserva_dono = db.query(
                PedidoReserva.PedidoResevaID,
                Recurso.RecursoID,
                Recurso.Nome,
                Utilizador.NomeUtilizador,
                PedidoReserva.DataInicio,
                PedidoReserva.DataFim,
                EstadoPedidoReserva.DescEstadoPedidoReserva
            ).join(
                Recurso, PedidoReserva.RecursoID == Recurso.RecursoID
            ).join(
                EstadoPedidoReserva, PedidoReserva.EstadoID == EstadoPedidoReserva.EstadoID
            ).join(
                Utilizador, PedidoReserva.UtilizadorID == Utilizador.UtilizadorID
            ).filter(
                Recurso.UtilizadorID == utilizador_id
            ).all()

        pedidos_reserva_solicitante = db.query(
                PedidoReserva.PedidoResevaID,
                Recurso.RecursoID,
                Recurso.Nome,
                Utilizador.NomeUtilizador,
                PedidoReserva.DataInicio,
                PedidoReserva.DataFim,
                EstadoPedidoReserva.DescEstadoPedidoReserva
            ).join(
                Recurso, PedidoReserva.RecursoID == Recurso.RecursoID
            ).join(
                EstadoPedidoReserva, PedidoReserva.EstadoID == EstadoPedidoReserva.EstadoID
            ).join(
                Utilizador, Utilizador.UtilizadorID == Recurso.UtilizadorID
            ).filter(
                PedidoReserva.UtilizadorID == utilizador_id
            ).all()

        return pedidos_reserva_dono, pedidos_reserva_solicitante

    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

#Confirma a entrega de um recurso para empréstimo (dono)
async def confirma_entrega_recurso_dono_db(db:session, reserva_id: int):
    try:
        reserva = db.query(Reserva).filter(Reserva.ReservaID == reserva_id).first()
        reserva.RecursoEntregueDono = True
        db.commit()
        return {'Entrega do produto registada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

#Confirma a receção de um recurso numa reserva (pessoa que vai usufrir do recurso)
async def confirma_rececao_recurso_db(db:session, reserva_id: int):
    try:
        reserva = db.query(Reserva).filter(Reserva.ReservaID == reserva_id).first()
        reserva.RecursoEntregueVizinho = True
        db.commit()

        return {'Receção do recurso registada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

#Confirma a entrega da caução ao dono do produto
async def confirma_entrega_caucao_db(db:session, reserva_id: int):
    try:
        reserva = db.query(Reserva).filter(Reserva.ReservaID == reserva_id).first()
        reserva.ConfirmarCaucaoVizinho = True
        db.commit()

        return {'Entrega da caução registada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

#Confirma a receção da caução por parte da pessoa que irá usar o produto
async def confirma_rececao_caucao_db(db:session, reserva_id: int):
    try:
        reserva = db.query(Reserva).filter(Reserva.ReservaID == reserva_id).first()
        reserva.ConfirmarCaucaoDono = True
        db.commit()

        return {'Receção da caução registada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

#Insere justificação relativa ao mau estado do produto e não entrega da caução
async def inserir_justificacao_caucao_db(db:session, reserva_id: int, justificacao: str):
    try:
        reserva = db.query(Reserva).filter(Reserva.ReservaID == reserva_id).first()
        reserva.JustificacaoEstadoProduto = justificacao
        db.commit()

        return {'Justificação registada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

#Indicação do bom estado do produto e que a caução será entregue
async def inserir_bom_estado_produto_e_devolucao_caucao(db:session, reserva_id: int):
    try:
        reserva = db.query(Reserva).filter(Reserva.ReservaID == reserva_id).first()
        reserva.DevolucaoCaucao = True
        reserva.EstadoRecurso = True
        db.commit()

        return {'Confirmação do bom estado do produto e notificação da devolução da caução registada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}
