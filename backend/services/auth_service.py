from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.user_schemas import UserRegistar, UserLogin
from db.repository.user_repo import get_id_role, create_user, user_exists, get_user_by_email
from utils.PasswordHasher import hash_password, verificar_password
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import os
import jwt

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES", 30))


def formatar_string(word: str) -> str:
    return word.strip()


def generate_jwt_token(user_id: int, email: str, role: str) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)

    # Claims token JWT
    payload = {
        "id": user_id,
        "email": email,
        "role": role,
        "exp": expiration_time
    }

    # Cria o token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def registar_utilizador(user: UserRegistar, db: Session):
    try:
        # Remove os espaços
        user.role = formatar_string(user.role)
        user.email = formatar_string(user.email)

        # Verifica se o utilizador já existe
        if await user_exists(db, user.email):
            return False, "Email já está em uso"

        # Obtém ID do cargo
        role_id = await get_id_role(db, user.role)
        if role_id is None:
            return False, "Cargo não encontrado"

        user.password, salt = hash_password(user.password)

        # Adicionar o utilizador na base de dados
        if await create_user(db, user, role_id, salt):
            return True, "Utilizador criado com sucesso"
        else:
            return False, "Erro ao criar o Utilizador"

    except Exception as e:
        raise RuntimeError(f"Erro registar_utilizador: {e}")

async def user_valido(db: Session, userL: UserLogin):
    userL.email = formatar_string(userL.email)

    # Verifica se o email existe
    if not await user_exists(db, userL.email):
        return False, "Email não registado"

    user = await get_user_by_email(db, userL.email)
    if not user:
        raise HTTPException(status_code=500, detail="Erro ao encontar utilizador")

    # Verifica a password e o salt
    if verificar_password(userL.password, user.passwordHash, user.salt):
        # Gera o token JWT
        return True, generate_jwt_token(user.utilizadorID, user.email, user.role)
    else:
        return False, "Password incorreta"