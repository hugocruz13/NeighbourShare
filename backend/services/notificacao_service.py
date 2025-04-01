from sqlalchemy.orm import Session
import backend.db.repository.notificacao_repo as notificacao_repo
from backend.db.models import Notificacao
import backend.db.session as session

async def cria_notificacao_service(db:Session, notificacao:Notificacao, user_id:int):
    return await notificacao_repo.cria_notificacao_db(db, notificacao, user_id)