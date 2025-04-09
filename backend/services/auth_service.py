from db.repository.user_repo import *
from schemas.user_schemas import UserJWT, User, UserLogin, ResetPassword
from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.repository.user_repo import get_id_role, create_user, user_exists, get_user_by_email
from utils.PasswordHasher import hash_password, verificar_password
from services.jwt_services import generate_jwt_token_login, generate_jwt_token_registo, generate_jwt_token_recovery
from services.email_service import send_verification_email, send_recovery_password_email


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

        # Adicionar o utilizador a dbase
        if await create_user(db, user, role_id):
            try:
                temp = get_user_by_email(db, user.email)
                if not temp:
                    raise RuntimeError("Erro ao obter utilizador")
                jwt_token = generate_jwt_token_registo(str(user.email), user.role, temp.utilizador_ID)
                send_verification_email(str(user.email), jwt_token)
                return True, "Registo realizado com sucesso"
            except Exception as e:
                await rollback_user(db, user.email)
                return False, f"Erro durante o envio de email ou geração do token: {e}"
        else:
            return False, "Erro ao criar o Utilizador"
    except Exception as e:
        raise RuntimeError(f"Erro registar_utilizador: {e}")

async def atualizar_novo_utilizador(user: NewUserUpdate, token:UserJWT, db: Session):
    try:
        if user_exists(db, str(token.email)):
            password_hashed, salt = hash_password(user.password)
            await update_new_user(db, user, token.id, password_hashed, salt)
            user.password = ""
            return True, "Utilizador atualizado com sucesso"
        else:
            return False, "Erro ao verificar utilizador"
    except Exception as e:
        raise RuntimeError(f"Erro atualizar novo utilizador: {e}")

async def user_login(db: Session, user: UserLogin):
    try:
        # Remove os espaços do email
        user.email = formatar_string(user.email)

        # Verifica se o email existe
        if not await user_exists(db, user_login.email):
            raise HTTPException(status_code=401, detail="Email não registado")

        # Vai a dbase buscar informações do utilizador
        dados = get_user_by_email(db, user.email)

        # Confirma se o utilizador foi encontrado
        if not dados:
            raise HTTPException(status_code=400, detail="Erro ao encontrar o utilizador")

        # Verifica a password e o salt
        if verificar_password(user.password, dados.password_hash, dados.salt):
            # Gera o token JWT
            return True, generate_jwt_token_login(dados.utilizador_ID, dados.email, dados.role)
        else:
            raise HTTPException(status_code=401, detail="Password incorreta")
    except Exception as e:
        raise e

async def verificao_utilizador(db: Session, user: UserJWT):
    try:
        return await user_exists(db, user.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def verificar_forgot(db: Session, email: str):
    try:
        if await user_exists(db, email):
            id_user = get_user_by_email(db, email).utilizador_ID
            token = generate_jwt_token_recovery(id_user, email)
            send_recovery_password_email(email, token)
        return "Se o endereço de email submetido estiver registado, irá receber um email com um link para alterar a password"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def atualizar_nova_password(db: Session, user:ResetPassword, token:UserJWT):
    try:
        if await user_exists(db, str(token.email)):
            password_hashed, salt = hash_password(user.password)
            await update_new_password(db, token.id, password_hashed, salt)
            user.password = ""
            return True, "Password atualizada com sucesso"
        else:
            return False, "Erro ao verificar utilizador"
    except Exception as e:
        raise RuntimeError(f"Erro atualizar novo utilizador: {e}")
