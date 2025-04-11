from sqlalchemy.orm import Session
from schemas.votacao_schema import Criar_Votacao
from db.models import Votacao

async def criar_votacao_no_db(db: Session, votacao: Criar_Votacao):
    try:
        votacao_new = Votacao(Titulo=votacao.titulo, Descricao=votacao.descricao, DataInicio=votacao.data_str, DataFim=votacao.data_end)
        db.add(votacao_new)
        db.commit()
        db.refresh(votacao_new)
        return True
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar utilizador: {e}")