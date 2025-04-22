from sqlalchemy.orm import joinedload
from db.models import PedidoNovoRecurso, PedidoManutencao, RecursoComun
from sqlalchemy.exc import SQLAlchemyError
import db.session as session
from schemas.recurso_comum_schema import *

#Inserção de um novo recurso comum
async def inserir_recurso_comum_db(db:session, recurso_comum:RecursoComumSchemaCreate):
    try:
        novo_recurso_comum = RecursoComun(Nome=recurso_comum.nome, DescRecursoComum=recurso_comum.descRecursoComum)
        db.add(novo_recurso_comum)
        db.commit()
        db.refresh(novo_recurso_comum)

        return {'Recurso comum inserido com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

#Inserção de um novo pedido de um novo recurso comum
async def inserir_pedido_novo_recurso_db(db:session, pedido:PedidoNovoRecursoSchemaCreate):
    try:
        novo_pedido = PedidoNovoRecurso(DescPedidoNovoRecurso=pedido.DescPedidoNovoRecurso, DataPedido=pedido.DataPedido, UtilizadorID=pedido.UtilizadorID, EstadoPedNovoRecID=pedido.EstadoPedNovoRecID)
        db.add(novo_pedido)
        db.commit()
        db.refresh(novo_pedido)

        return {'Pedido de novo recurso inserido com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

#Inserção de um pedido de manutenção de um recurso comum
async def inserir_pedido_manutencao_db(db:session, pedido:PedidoManutencaoSchemaCreate):
    try:
        novo_pedido = PedidoManutencao(**pedido.dict())
        db.add(novo_pedido)
        db.commit()
        db.refresh(novo_pedido)

        return {'Pedido de manutenção inserido com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

async def listar_pedidos_novos_recursos_db(db:session):
    try:
        pedidos_novos_recursos = (
            db.query(PedidoNovoRecurso)
            .options(
                joinedload(PedidoNovoRecurso.Utilizador_),
                joinedload(PedidoNovoRecurso.EstadoPedidoNovoRecurso_)
            )
            .all()
        )
        return pedidos_novos_recursos

    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def listar_pedidos_novos_recursos_pendentes_db(db:session):
    try:
        pedidos_novos_recursos_pendentes = (
            db.query(PedidoNovoRecurso)
            .options(
                joinedload(PedidoNovoRecurso.Utilizador_),
                joinedload(PedidoNovoRecurso.EstadoPedidoNovoRecurso_)
            )
            .filter(PedidoNovoRecurso.EstadoPedNovoRecID == 1)
            .all()
        )

        return pedidos_novos_recursos_pendentes
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def listar_pedidos_novos_recursos_aprovados_db(db:session):
    try:
        pedidos_novos_recursos_aprovados = (
            db.query(PedidoNovoRecurso)
            .options(
                joinedload(PedidoNovoRecurso.Utilizador_),
                joinedload(PedidoNovoRecurso.EstadoPedidoNovoRecurso_)
            )
            .filter(PedidoNovoRecurso.EstadoPedNovoRecID == 2)
            .all()
        )

        return pedidos_novos_recursos_aprovados

    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def listar_pedidos_manutencao_db(db:session):

    try:
        pedidos_manutencao = (
            db.query(PedidoManutencao)
            .options(
                joinedload(PedidoManutencao.Utilizador_),
                joinedload(PedidoManutencao.EstadoPedidoManutencao_),
                joinedload(PedidoManutencao.RecursoComun_)
            )
            .all()
        )

        return pedidos_manutencao

    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def listar_pedidos_manutencao_em_progresso_db(db:session):

    try:
        pedidos_manutencao_em_progresso = (
            db.query(PedidoManutencao)
            .options(
                joinedload(PedidoManutencao.Utilizador_),
                joinedload(PedidoManutencao.EstadoPedidoManutencao_),
                joinedload(PedidoManutencao.RecursoComun_)
            )
            .filter(PedidoManutencao.EstadoPedManuID == 1)
            .all()
        )

        return pedidos_manutencao_em_progresso

    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def listar_pedidos_manutencao_finalizados_db(db:session):
    try:
        pedidos_manutencao_finalizado = (
            db.query(PedidoManutencao)
            .options(
                joinedload(PedidoManutencao.Utilizador_),
                joinedload(PedidoManutencao.EstadoPedidoManutencao_),
                joinedload(PedidoManutencao.RecursoComun_)
            )
            .filter(PedidoManutencao.EstadoPedManuID == 2)
            .all()
        )

        return pedidos_manutencao_finalizado

    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))
