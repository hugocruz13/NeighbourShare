from fastapi.params import Depends
from sqlalchemy.orm import joinedload
from backend.db import session
from backend.db.models import Recurso
from sqlalchemy.exc import SQLAlchemyError

async def listar_recursos_db(db:session):
    try:
        recursos = (
            db.query(Recurso)
            .options(
                joinedload(Recurso.Utilizador_),
                joinedload(Recurso.Categoria_),
                joinedload(Recurso.Disponibilidade_)
            )
            .all()
        )
        return recursos
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def listar_recursos_disponiveis_db(db:session):
    try:
        recursos_disponiveis = (
            db.query(Recurso)
            .filter(Recurso.DispID == 1)
            .options(
                joinedload(Recurso.Utilizador_),
                joinedload(Recurso.Categoria_),
                joinedload(Recurso.Disponibilidade_)
            )
        )
        return recursos_disponiveis
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def listar_recursos_indisponiveis(db:session):
    try:
        recursos_indisponiveis = (
            db.query(Recurso)
            .filter(Recurso.DispID == 2)
            .options(
                joinedload(Recurso.Utilizador_),
                joinedload(Recurso.Categoria_),
                joinedload(Recurso.Disponibilidade_)
            )
        )
        return recursos_indisponiveis
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))