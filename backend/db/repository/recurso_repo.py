from sqlalchemy.orm import joinedload
from db import session
from db.models import Recurso, Disponibilidade, Categoria
from sqlalchemy.exc import SQLAlchemyError

def get_disponibilidade_id_db(disponibilidade:str, db:session):
    try:
            disponibilidade_id = db.query(Disponibilidade).filter(Disponibilidade.DescDisponibilidade == disponibilidade).first().DispID
            if disponibilidade_id:
                return disponibilidade_id
            else:
                raise Exception("Nenhuma disponibilidade encontrada com o nome informado")
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

def get_categoria_id_db(categoria:str, db:session):
    try:
        categoria_id = db.query(Categoria).filter(Categoria.DescCategoria == categoria).first().CatID
        if categoria_id:
            return categoria_id
        else:
            raise Exception("Nenhuma categoria encontrada com o nome informado")
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

async def inserir_recurso_db(db:session, recurso:Recurso):
    try:
        novo_recurso = Recurso(
            Nome=recurso.Nome,
            DescRecurso=recurso.DescRecurso,
            Caucao=recurso.Caucao,
            UtilizadorID=recurso.UtilizadorID,
            DispID = recurso.DispID,
            CatID=recurso.CatID
        )
        db.add(novo_recurso)
        db.commit()
        db.refresh(novo_recurso)

        return novo_recurso.RecursoID, {'Inserção do recurso realizada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return False, {'details': str(e)}

#Lista todos os recursos registados no sistema
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

#Lista as informações referentes a um recurso registado no sistema
async def listar_recurso_db(db:session, recurso_id:int):
    try:
        recurso = db.query(Recurso).filter(Recurso.RecursoID == recurso_id).first()
        return recurso
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

#Lista os recursos pertencentes a um utilizador (utilizador_id)
async def listar_recursos_utilizador_db(db:session, utilizador_id:int):
    try:
        recursos = (
            db.query(Recurso)
            .filter(Recurso.UtilizadorID == utilizador_id)
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