from sqlalchemy.orm import joinedload
from backend.db.session import get_db
from backend.db.models import RecursoComun, PedidoNovoRecurso, PedidoManutencao
from sqlalchemy.exc import SQLAlchemyError
import backend.db.session as session

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
        return pedidos_novos_recursos , {"Consulta efetuada com sucesso!"}

    except SQLAlchemyError as e:
        return False, {'details': str(e)}

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

        return pedidos_novos_recursos_pendentes, {"Consulta efetuada com sucesso!"}
    except SQLAlchemyError as e:
        return False, {'details': str(e)}

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

        return pedidos_novos_recursos_aprovados, {"Consulta efetuada com sucesso!"}

    except SQLAlchemyError as e:
        return False, {'details': str(e)}

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

        return pedidos_manutencao, {"Consulta efetuada com sucesso!"}

    except SQLAlchemyError as e:
        return False, {'details': str(e)}

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

        return pedidos_manutencao_em_progresso, {"Consulta efetuada com sucesso!"}

    except SQLAlchemyError as e:
        return False, {'details': str(e)}

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

        return pedidos_manutencao_finalizado, {"Consulta efetuada com sucesso!"}

    except SQLAlchemyError as e:
        return False, {'details': str(e)}
