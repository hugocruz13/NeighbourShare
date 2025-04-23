from datetime import datetime, date
from sqlalchemy.orm import Session
from schemas.votacao_schema import Criar_Votacao_Novo_Recurso, Criar_Votacao_Pedido_Manutencao, Votar_id, Consulta_Votacao
from db.models import Votacao, PedidoNovoRecurso, PedidoManutencao, Voto


async def criar_votacao_nr_db(db: Session, votacao: Criar_Votacao_Novo_Recurso):
    try:
        votacao_new = Votacao(Titulo=votacao.titulo, Descricao=votacao.descricao, DataInicio=date.today(), DataFim=votacao.data_fim)
        pedido = db.query(PedidoNovoRecurso).filter(PedidoNovoRecurso.PedidoNovoRecID == votacao.id_pedido).first()

        if not pedido:
            raise RuntimeError(f"Pedido com ID {votacao.id_pedido} não encontrado.")

        db.add(votacao_new)
        db.commit()
        db.refresh(votacao_new)

        pedido.VotacaoID = votacao_new.VotacaoID
        db.commit()

        return True

    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar votação: {e}")

async def criar_votacao_pedido_manutencao_db(db: Session, votacao: Criar_Votacao_Pedido_Manutencao):
    try:
        votacao_new = Votacao(Titulo=votacao.titulo, Descricao=votacao.descricao, DataInicio=date.today(), DataFim=votacao.data_fim)
        pedido_manutencao = db.query(PedidoManutencao).filter(PedidoManutencao.PMID == votacao.id_pedido_manutencao).first()

        if not pedido_manutencao:
            raise RuntimeError(f"Manutenção com ID {votacao.id_pedido_manutencao} não encontrado.")

        db.add(votacao_new)
        db.commit()
        db.refresh(votacao_new)

        pedido_manutencao.VotacaoID = votacao_new.VotacaoID
        db.commit()

        return True

    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar votação: {e}")

async def registar_voto(db: Session, voto:Votar_id):
    try:
        voto_new = Voto(VotacaoID=voto.id_votacao, UtilizadorID=voto.id_user, EscolhaVoto=voto.voto, DataVoto=datetime.today())
        db.add(voto_new)
        db.commit()
        db.refresh(voto_new)
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

async def existe_pedido_manutencao(db: Session, id:int):
    try:
        query = db.query(PedidoManutencao).filter(PedidoManutencao.PMID == id).first()
        return True if query else False
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar utilizador: {e}")

async def existe_votacao(db: Session, id:int):
    try:
        query = db.query(Votacao).filter(Votacao.VotacaoID==id).first()
        return True if query else False
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar utilizador: {e}")

def ja_votou(db: Session, votacao: Consulta_Votacao) -> bool:
    try:
        query = db.query(Voto).filter(Voto.VotacaoID == votacao.id_votacao,Voto.UtilizadorID == votacao.id_user).first()
        return query is not None
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao verificar se já votou: {e}")