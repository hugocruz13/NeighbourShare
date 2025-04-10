from sqlalchemy.orm import joinedload
from db import session
from db.models import PedidoReserva, Reserva
from schemas.reserva_schema import *
from sqlalchemy.exc import SQLAlchemyError

async def criar_pedido_reserva_db(db:session, pedido_reserva : PedidoReservaSchemaCreate):

    try:
        novo_pedido_reserva = PedidoReserva(
            UtilizadorID= pedido_reserva.Utilizador_.UtilizadorID,
            RecursoID= pedido_reserva.Recurso_.RecursoID,
            DataInicio= pedido_reserva.DataInicio,
            DataFim= pedido_reserva.DataFim
        )

        db.add(novo_pedido_reserva)
        db.commit()
        db.refresh(novo_pedido_reserva)

        return {'Pedido de reserva criado com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

# Mostra os pedidos de reserva efetuados por um utilizador (utilizador_id)
async def lista_pedidos_reserva_db(db:session, utilizador_id: int):
    try:
        pedidos_reserva = (
            db.query(PedidoReserva)
            .options(
                joinedload(PedidoReserva.Recurso_),
                joinedload(PedidoReserva.Utilizador_),
                joinedload(PedidoReserva.EstadoPedidoReserva_)
            )
            .filter(PedidoReserva.UtilizadorID == utilizador_id)
        )
        return pedidos_reserva
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

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

async def cria_reserva_db(db:session, reserva:ReservaSchemaCreate):
    try:
        nova_reserva = Reserva(
            PedidoResevaID=reserva.PedidoReserva_.PedidoResevaID
        )

        db.add(nova_reserva)
        db.commit()
        db.refresh(nova_reserva)

        return {'Reserva criada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

async def get_reserva_db(db:session, reserva_id: int):
    try:
        reserva = db.query(Reserva).filter(Reserva.ReservaID == reserva_id).first()
        return reserva
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

# Mostra as reservas onde o utilizador (utilizador_id) contêm um recurso emprestado consigo
async def lista_reservas_db(db:session, utilizador_id: int):
    try:
        reservas = (
            db.query(Reserva)
            .options(
                joinedload(Reserva.PedidoReserva_)
            )
            .filter(PedidoReserva.UtilizadorID == utilizador_id, PedidoReserva.EstadoID == 1)
        )

        return reservas
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
        reserva.JustificacaoMauEstado = justificacao
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
