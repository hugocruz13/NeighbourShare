from fastapi import  HTTPException
from schemas import  UserLogin
from db.repository.user_repo import *
from utils.PasswordHasher import hash_password, verificar_password
from services.jwt_services import generate_jwt_token

def formatar_string(word: str) -> str:
    return word.strip()

async def registar_utilizador(user: UserRegistar, db: Session):
    try:
        # Remove os espaços
        user.role = formatar_string(user.role)
        user.email = formatar_string(user.email)

        # Verifica se o utilizador já existe
        if await user_exists(db, user.email):
            return False, "Email registado"

        # Obtém ID do role
        role_id = await get_id_role(db, user.role)
        if role_id is None:
            return False, "Permissões não existe"

        # Converte a password num hash e salt
        user.password, salt = hash_password(user.password)

        # Adicionar o utilizador a db
        if await create_user(db, user, role_id, salt):
            return True, "Registo realizado com sucesso"
        else:
            return False, "Erro ao criar o Utilizador"
    except Exception as e:
        raise RuntimeError(f"Erro registar_utilizador: {e}")

async def user_valido(db: Session, user_login: UserLogin):

    # Remove os espaços do email
    user_login.email = formatar_string(user_login.email)

    # Verifica se o email existe
    if not await user_exists(db, user_login.email):
        return False, "Email não registado"

    # Vai a db buscar informações do utilizador
    user = await get_user_by_email(db, user_login.email)

    # Confirma se o utilizador foi encontrado
    if not user:
        raise HTTPException(status_code=500, detail="Erro ao encontar utilizador")

    # Verifica a password e o salt
    if verificar_password(user_login.password, user.passwordHash, user.salt):
        # Gera o token JWT
        return True, generate_jwt_token(user.utilizadorID, user.email, user.role)
    else:
        return False, "Password incorreta"