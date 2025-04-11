from schemas.votacao_schema import Criar_Votacao, Pedido_Novo_Recurso
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.string_utils import formatar_string
from db.repository.votacao_repo import criar_votacao_no_db, criar_votacao_nr, existe_nr, existe_vot

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

async def votacao_nr(db: Session, votacao: Pedido_Novo_Recurso):
    try:
        if not await existe_nr(db, votacao.id_pedido):
            raise HTTPException(status_code=404, detail="Erro ao encontar pedido")

        if not await existe_vot(db, votacao.id_votacao):
            raise HTTPException(status_code=404, detail="Erro ao encontar votação")

        return await criar_votacao_nr(db,votacao)
    except Exception as e:
        raise e