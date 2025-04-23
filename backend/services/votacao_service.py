from datetime import date
from schemas.votacao_schema import Criar_Votacao, Votar_id, Consulta_Votacao
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.string_utils import formatar_string
from db.repository.votacao_repo import criar_votacao_nr_db, criar_votacao_pedido_manutencao_db, existe_nr, existe_pedido_manutencao, \
    existe_votacao, registar_voto, ja_votou

#criar votação
async def gerir_votacao_novo_recurso(db: Session, votacao: Criar_Votacao):
    try:
        #Formata as strings e remove espaços desnecessários
        votacao.titulo = formatar_string(votacao.titulo)
        votacao.descricao = formatar_string(votacao.descricao)

        #Verifica se o pedido existe
        if not await existe_nr(db, votacao.id_processo):
            raise HTTPException(status_code=404, detail="Erro ao encontar pedido")

        #Verifica se a votação tem no mínimo 1 dia,
        if votacao.data_fim<= date.today():
            raise HTTPException(status_code=400, detail="A data de fim da votação deve ser posterior à data de início (mínimo 1 dia de duração).")


        return await criar_votacao_nr_db(db,votacao)
    except Exception as e:
        raise e

async def gerir_votacao_pedido_manutencao(db: Session, votacao: Criar_Votacao):
    try:
        #Formata as strings e remove espaços desnecessários
        votacao.titulo = formatar_string(votacao.titulo)
        votacao.descricao = formatar_string(votacao.descricao)

        #Verifica se o pedido de manutenção existe
        if not await existe_pedido_manutencao(db, votacao.id_processo):
            raise HTTPException(status_code=404, detail="Erro ao encontar manutenção")

        #Verifica se a votação tem no mínimo 1 dia,
        if votacao.data_fim<= date.today():
            raise HTTPException(status_code=400, detail="A data de fim da votação deve ser posterior à data de início (mínimo 1 dia de duração).")

        return await criar_votacao_pedido_manutencao_db(db,votacao)
    except Exception as e:
        raise e

#votar
async def gerir_voto(db: Session, voto:Votar_id):
    try:
        #Formata as strings e remove espaços desnecessários
        voto.voto = formatar_string(voto.voto)

        #Verifica se a votação existe
        if not await existe_votacao(db, voto.id_votacao):
            raise HTTPException(status_code=404, detail="Erro ao encontar votação")

        if ja_votou(db, Consulta_Votacao(id_votacao=voto.id_votacao, id_user=voto.id_user)):
            raise HTTPException(status_code=403, detail="Utilizador já registou a votação")

        return await registar_voto(db,voto)
    except Exception as e:
        raise e