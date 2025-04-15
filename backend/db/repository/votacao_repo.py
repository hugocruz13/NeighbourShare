from sqlalchemy.orm import Session
from schemas.votacao_schema import Criar_Votacao
from db.models import Votacao, PedidoNovoRecurso


async def criar_votacao_no_db(db: Session, votacao: Criar_Votacao):
    try:
        votacao_new = Votacao(Titulo=votacao.titulo, Descricao=votacao.descricao, DataInicio=votacao.data_str, DataFim=votacao.data_end)
        pedido = db.query(PedidoNovoRecurso).filter(PedidoNovoRecurso.PedidoNovoRecID == votacao.id_pedido).first()

        if not pedido:
            raise RuntimeError(f"Pedido com ID {votacao.id_pedido} não encontrado.")

        votacao_new.PedidoNovoRecurso.append(pedido)
        db.add(votacao_new)
        db.commit()
        db.refresh(votacao_new)

        return True

    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar votação: {e}")


async def existe_nr(db: Session, id:int):
    try:
        query = db.query(PedidoNovoRecurso).filter(PedidoNovoRecurso.PedidoNovoRecID == id).first()
        return True if query else False
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar utilizador: {e}")

async def existe_vot(db: Session, id:int):
    try:
        query = db.query(Votacao).filter(Votacao.VotacaoID == id).first()
        return True if query else False
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar utilizador: {e}")