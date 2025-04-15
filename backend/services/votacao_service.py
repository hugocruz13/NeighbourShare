from schemas.votacao_schema import Criar_Votacao
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.string_utils import formatar_string
from db.repository.votacao_repo import criar_votacao_no_db, existe_nr, existe_vot

async def gerir_votacao(db: Session, votacao: Criar_Votacao):
    try:
        #Formata as strings e remove espaços desnecessários
        votacao.titulo = formatar_string(votacao.titulo)
        votacao.descricao = formatar_string(votacao.descricao)

        #Verifica se o pedido existe
        if not await existe_nr(db, votacao.id_pedido):
            raise HTTPException(status_code=404, detail="Erro ao encontar pedido")

        #Verifica se a votação tem no mínimo 1 dia,
        if votacao.data_end <= votacao.data_str:
            raise HTTPException(status_code=400, detail="A data de fim da votação deve ser posterior à data de início (mínimo 1 dia de duração).")

        return await criar_votacao_no_db(db,votacao)
    except Exception as e:
        raise e
