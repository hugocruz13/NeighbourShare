from http.client import HTTPException

from requests import Session
from sqlalchemy.orm import joinedload
from db.models import PedidoNovoRecurso, PedidoManutencao, RecursoComun, EstadoPedidoManutencao, EstadoManutencao, \
    Manutencao, EntidadeExterna
from sqlalchemy.exc import SQLAlchemyError
import db.session as session
from schemas.recurso_comum_schema import *

#region Gestão de Recursos Comuns

#Inserção de um novo recurso comum
async def inserir_recurso_comum_db(db:session, recurso_comum:RecursoComumSchemaCreate):
    try:
        novo_recurso_comum = RecursoComun(**recurso_comum.dict())
        db.add(novo_recurso_comum)
        db.commit()
        db.refresh(novo_recurso_comum)

        return {'Recurso comum inserido com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'details': str(e)}

#endregion

#region Pedidos de Novos Recursos Comuns

#Inserção de um novo pedido de um novo recurso comum
async def inserir_pedido_novo_recurso_db(db:session, pedido:PedidoNovoRecursoSchemaCreate):
    try:
        novo_pedido = PedidoNovoRecurso(**pedido.dict())
        db.add(novo_pedido)
        db.commit()
        db.refresh(novo_pedido)

        return {'Pedido de novo recurso inserido com sucesso!'}
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

async def obter_pedido_novo_recurso_db(db:session, id_pedido: int):
    try:
        pedido_novo_recurso = db.query(PedidoNovoRecurso).filter(PedidoNovoRecurso.PedidoNovoRecID == id_pedido).first()
        return pedido_novo_recurso
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

#endregion

#region Pedidos de Manutenção

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

async def obter_all_tipo_estado_pedido_manutencao(db:session):
    try:
        dbc = db.query(EstadoPedidoManutencao).all()
        if dbc is None:
            return None
        return dbc
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def alterar_estado_pedido_manutencao(db:session, id_pedido_manutencao:int, estado_pedido_manutencao:int):
    try:
        pedido_manutencao = db.query(PedidoManutencao).filter(PedidoManutencao.PMID == id_pedido_manutencao).first()
        pedido_manutencao.EstadoPedManuID = estado_pedido_manutencao
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(str(e))

async def obter_pedido_manutencao_db(db:session, id_manutencao:int):
    try:
        pedido_manutencao = db.query(PedidoManutencao).filter(PedidoManutencao.PMID == id_manutencao).first()
        return pedido_manutencao
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def update_pedido_manutencao_db(db:session, u_pedido: PedidoManutencaoUpdateSchema):
    pedido = db.query(PedidoManutencao).filter(PedidoManutencao.PMID == u_pedido.PMID).first()
    pedido.DescPedido = u_pedido.DescPedido
    db.commit()
    return pedido

async def eliminar_pedido_manutencao(db:session, pedido_id:int):
    try:
        pedido_manutencao = db.query(PedidoManutencao).filter(PedidoManutencao.PMID == pedido_id).first()
        db.delete(pedido_manutencao)
        db.commit()
        return {'Pedido de manutenção eliminado com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(str(e))

#endregion

#region Manutenção de Recursos Comuns

async def criar_manutencao_db(db:session, manutencao:ManutencaoCreateSchema):
    try:
        nova_manutencao = Manutencao(
            PMID=manutencao.PMID,
            EntidadeID=manutencao.EntidadeID,
            DataManutencao=manutencao.DataManutencao,
            DescManutencao=manutencao.DescManutencao
        )

        db.add(nova_manutencao)
        db.commit()

        return {'Nova manutenção adicionada com sucesso !'}

    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def obter_all_tipo_estado_manutencao(db:session):
    try:
        dbc = db.query(EstadoManutencao).all()
        if dbc is None:
            return None
        return dbc
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def alterar_estado_manutencao(db:session, id_manutencao:int, tipo_estado_manutencao:int):
    try:
        manutencao = db.query(Manutencao).filter(Manutencao.PMID == id_manutencao).first()
        manutencao.TipoManuID = tipo_estado_manutencao
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(str(e))

async def obter_manutencao_db(db:session, id_manutencao:int):
    try:
        manutencao = db.query(Manutencao).filter(Manutencao.PMID == id_manutencao).first()
        return manutencao
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def listar_manutencoes_db(db:session):
    try:
        manutencoes = db.query(Manutencao).all()
        return manutencoes
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def update_manutencao_db(db:session, u_manutencao: ManutencaoUpdateSchema):
    manutencao = db.query(Manutencao).filter(Manutencao.ManutencaoID == u_manutencao.ManutencaoID).first()
    entidades = db.query(EntidadeExterna).all()
    pmid = db.query(PedidoManutencao).all()
    for e in entidades:
        if e.EntidadeID != u_manutencao.EntidadeID:
            return None
    for e in pmid:
        if e.PMID != u_manutencao.PMID:
            return None
    manutencao.PMID = u_manutencao.PMID
    manutencao.EntidadeID = u_manutencao.EntidadeID
    manutencao.DataManutencao = u_manutencao.DataManutencao
    manutencao.DescManutencao = u_manutencao.DescManutencao

    db.commit()
    return manutencao

#Eliminar uma manutenção da base de dados
async def eliminar_manutencao_db(db:session, id_manutencao:int):
    try:
        manutencao = db.query(Manutencao).filter(Manutencao.ManutencaoID == id_manutencao).first()
        db.delete(manutencao)
        db.commit()

        return {'Manutenção eliminada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(str(e))

#endregion



