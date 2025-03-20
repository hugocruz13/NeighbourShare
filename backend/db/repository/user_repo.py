from sqlalchemy.orm import Session
from db.models import Utilizador, TipoUtilizador
from schemas.user_schemas import *

def get_user_by_email(db: Session, user: UserBase):
    query = db.query(Utilizador).filter(Utilizador.Email == user.email).first()
    response = UserResponse(
        email=query.Email,
        tipo=query.TUID,
        id=query.UtilizadorID
    )
    return response

def create_user(db: Session, user: UserRegistar, id_role: int, salt:str):
    new_user = Utilizador(NomeUtilizador=user.nome,DataNasc=user.data_nasc,Email=user.email, Contacto=user.contacto, PasswordHash=user.password, Salt=salt, Foto=user.foto, TUID=id_role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_id_role(db: Session, role: str):
    query = db.query(TipoUtilizador).filter(TipoUtilizador.DescTU == role).first()
    return query.TUID