import datetime
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from db.models import Utilizador, TipoUtilizador
from schemas.user_schemas import UserRegistar, User, NewUserUpdate, UserUpdateInfo, UserData

async def create_user(db: Session, user: UserRegistar, id_role: int):
    try:
        date = datetime.date.today()
        new_user = Utilizador(NomeUtilizador="none", DataNasc=date, Email=str(user.email), Contacto=0, PasswordHash="none", Salt="none", TUID=id_role, Verificado=False, Path="none")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def rollback_user(db: Session, email: EmailStr):
    try:
        db.query(Utilizador).filter(Utilizador.Email == email).delete()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def update_new_password(db: Session, user_identifier: int, password_hashed: str,salt: str):
    try:
        new_user = db.query(Utilizador).filter(Utilizador.UtilizadorID == user_identifier).first()
        if new_user:
            new_user.PasswordHash = password_hashed
            new_user.Salt = salt
            db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def update_new_user(db: Session, user: NewUserUpdate, user_identifier: int, password_hashed: str,salt: str, path: str):
    try:
        new_user = db.query(Utilizador).filter(Utilizador.UtilizadorID == user_identifier).first()
        if new_user:
            if user.nome is not None:
                new_user.NomeUtilizador = user.nome
            if user.data_nascimento is not None:
                new_user.DataNasc=user.data_nascimento
            if user.contacto is not None:
                new_user.Contacto=user.contacto
            if password_hashed is not None:
                new_user.PasswordHash = password_hashed
            if salt is not None:
                new_user.Salt = salt
            new_user.Path = path
            new_user.Verificado = True
            db.commit()
        else:
            raise RuntimeError("ID do utilizador inválido!")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def get_id_role(db: Session, role: str):
    try:
        query = db.query(TipoUtilizador).filter(TipoUtilizador.DescTU == role).first()
        return query.TUID if query else None
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def user_exists(db: Session, email: str):
    try:
        return db.query(Utilizador).filter(Utilizador.Email == email).first() is not None
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_user_by_email(db: Session, email: str):
    try:
        user = db.query(Utilizador).filter(Utilizador.Email == email).first()
        if user:
            role = user.TipoUtilizador_.DescTU if user.TipoUtilizador_ else None
            return User(
                utilizador_ID=user.UtilizadorID,
                email=user.Email,
                password_hash = user.PasswordHash,
                salt=user.Salt,
                role=role
            )
        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def apagar(db: Session, id: int):
    try:
        utilizador = db.query(Utilizador).filter(Utilizador.UtilizadorID == id).first()
        if utilizador:
            db.delete(utilizador)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Função para obter os dados aquando da consulta de perfil do utilizador
async def get_dados_utilizador(db:Session, id_user:int):
    try:
        utilizador = db.query(Utilizador).filter(Utilizador.UtilizadorID == id_user).first()
        if utilizador:
            return UserData(
                nome=str(utilizador.NomeUtilizador),
                email=str(utilizador.Email),
                contacto= utilizador.Contacto,
                data_nascimento=utilizador.DataNasc,
                imagem=utilizador.Path,
            )
        else:
            return None
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Função que obtêm os ID's de todos os admins/gestores
async def get_all_admin_gestores_ids(db:Session):
    try:
        lista_ids = db.query(Utilizador.UtilizadorID).filter(TipoUtilizador.DescTU != "residente").all()
        return lista_ids
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def atualizar_utilizador_db(db: Session, id: int,dados: UserUpdateInfo):
    try:
        user = db.query(Utilizador).filter(Utilizador.UtilizadorID == id).first()
        if not user:
            return False
        if dados.nome is not None and dados.nome != "":
            user.NomeUtilizador = dados.nome
        if dados.contacto is not None and dados.contacto != 0:
            user.Contacto = dados.contacto
        if dados.data_nascimento is not None and dados.data_nascimento != datetime.date.today():
            user.DataNasc = dados.data_nascimento
        db.commit()
        db.refresh(user)
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))