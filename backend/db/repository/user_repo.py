from pydantic import EmailStr
from sqlalchemy.orm import Session
from db.models import Utilizador, TipoUtilizador
from schemas.user_schemas import UserRegistar, User

async def create_user(db: Session, user: UserRegistar, id_role: int, salt:str):
    try:
        new_user = Utilizador(NomeUtilizador=user.nome, DataNasc=user.data_nasc, Email=user.email, Contacto=user.contacto, PasswordHash=user.password, Salt=salt, TUID=id_role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return True
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar utilizador: {e}")

async def get_id_role(db: Session, role: str):
    try:
        query = db.query(TipoUtilizador).filter(TipoUtilizador.DescTU == role).first()
        return query.TUID if query else None
    except Exception as e:
        raise RuntimeError(f"Erro ao obter ID do cargo: {e}")

async def user_exists(db: Session, email: str):
    try:
        return db.query(Utilizador).filter(Utilizador.Email == email).first() is not None
    except Exception as e:
        raise RuntimeError(f"Erro ao verificar utilizador: {e}")

async def get_user_by_email(db: Session, email: EmailStr):
    try:
        user = db.query(Utilizador).filter(Utilizador.Email == email).first()
        if user:
            role = user.TipoUtilizador_.DescTU if user.TipoUtilizador_ else None
            return User(
                utilizadorID=user.UtilizadorID,
                email=user.Email,
                passwordHash = user.PasswordHash,
                salt=user.Salt,
                role=role
            )
        return None
    except Exception as e:
        raise RuntimeError(f"Erro ao obter utilizador: {e}")