from sqlalchemy.orm import Session
import db.repository.notificacao_repo as notificacao_repo
from db.models import Notificacao
from fastapi import HTTPException

async def cria_notificacao_individual_service(db:Session, notificacao:Notificacao, user_id:int):
    return await notificacao_repo.cria_notificacao_individual_db(db, notificacao, user_id)

async def cria_notificacao_admin_service(db:Session, notificacao:Notificacao):
    return await notificacao_repo.cria_notificacao_admin_db(db, notificacao)

async def cria_notificacao_todos_service(db:Session, notificacao:Notificacao):
    return await notificacao_repo.cria_notificacao_todos_utilizadores_db(db,notificacao)

async def listar_notificacoes_service(db:Session, user_id:int):

    lista_notificacoes = await notificacao_repo.listar_notificacoes_db(db, user_id)

    if not lista_notificacoes:
        raise HTTPException(status_code=400, detail="Nenhuma notificação encontrada")

    return lista_notificacoes
