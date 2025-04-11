from sqlalchemy.orm import Session
from schemas.votacao_schema import Criar_Votacao, Return_Votacao, Pedido_Novo_Recurso
from db.models import Votacao, PedidoNovoRecurso

async def criar_votacao_no_db(db: Session, votacao: Criar_Votacao):
    try:
        votacao_new = Votacao(Titulo=votacao.titulo, Descricao=votacao.descricao, DataInicio=votacao.data_str, DataFim=votacao.data_end)
        db.add(votacao_new)
        db.commit()
        db.refresh(votacao_new)
        last = db.query(Votacao).order_by(Votacao.VotacaoID.desc()).first()
        return Return_Votacao(id=last.VotacaoID,titulo=last.Titulo,descricao=last.Descricao,data_str=last.DataInicio,data_end=last.DataFim)
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar utilizador: {e}")

#fix
async def criar_votacao_nr(db: Session, votacao: Pedido_Novo_Recurso):
    try:
        votacao_new = VotacaoPedidoNovoRecurso(VotacaoID=votacao.id_votacao,PedidoNovoRecID=votacao.id_pedido)
        db.add(votacao_new)
        db.commit()
        db.refresh(votacao_new)
        return True
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar utilizador: {e}")

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