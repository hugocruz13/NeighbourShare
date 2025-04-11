from schemas.votacao_schema import Criar_Votacao
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.string_utils import formatar_string
from db.repository.votacao_repo import criar_votacao_no_db

async def gerir_votacao(db: Session, votacao: Criar_Votacao):
    try:
        votacao.titulo = formatar_string(votacao.titulo)
        votacao.descricao = formatar_string(votacao.descricao)

        # Garantir que a votação tem no minimo 1 dia
        #if (votacao.data_str >= votacao.data_end):
            #raise HTTPException(status_code=400, detail="A votação deve ter pelo menos 1 dia de duração.")

        return await criar_votacao_no_db(db,votacao)
    except Exception as e:
        raise e