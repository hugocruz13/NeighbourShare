from sqlalchemy.orm import Session
import db.repository.notificacao_repo as notificacao_repo
from db.models import Notificacao

async def cria_notificacao_service(db:Session, notificacao:Notificacao, user_id:int):
    return await notificacao_repo.cria_notificacao_db(db, notificacao, user_id)