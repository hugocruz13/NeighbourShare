from requests import session
from sqlalchemy.sql.sqltypes import NULLTYPE

from db.repository.user_repo import *

from schemas.user_schemas import UserJWT, User, UserLogin, ResetPassword, UserData, UserUpdateInfo

from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.repository.user_repo import get_id_role, create_user, user_exists, get_user_by_email, apagar, atualizar_utilizador_db
from utils.PasswordHasher import hash_password, verificar_password
from services.jwt_services import generate_jwt_token_login, generate_jwt_token_registo, generate_jwt_token_recovery
from services.email_service import send_verification_email, send_recovery_password_email
from utils.tokens_record import add_save_token
from utils.string_utils import formatar_string


async def get_user_data(db: Session, id_user:int):

    return await get_dados_utilizador(db, id_user)

async def get_user_data(db: Session, id_user:int):

    return await get_dados_utilizador(db, id_user)

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
            return False, "Cargo inserido inválido"

        # Adicionar o utilizador a dbase
        if await create_user(db, user, role_id):
            try:
                temp = get_user_by_email(db, user.email)
                if not temp:
                    raise RuntimeError("Erro ao obter utilizador")
                jwt_token, exp = generate_jwt_token_registo(str(user.email), user.role, temp.utilizador_ID)
                send_verification_email(str(user.email), jwt_token)
                add_save_token(jwt_token, temp.utilizador_ID, str(user.email), "verification", exp)
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
        if await user_exists(db, str(token.email)):
            password_hashed, salt = hash_password(user.password)
            await update_new_user(db, user, token.id, password_hashed, salt)
            user.password = ""
            return True, "Utilizador atualizado com sucesso"
        else:
            return False, "Erro ao verificar utilizador"
    except Exception as e:
        raise RuntimeError(f"Erro atualizar novo utilizador: {e}")

async def user_auth(db: Session, user_login: UserLogin):
    try:
        # Remove os espaços do email
        user_login.email = formatar_string(user_login.email)

        # Verifica se o email existe
        if not await user_exists(db, user_login.email):
            raise HTTPException(status_code=401, detail="Email não registado")

        # Vai a db buscar informações do utilizador
        user = get_user_by_email(db, user_login.email)

        # Confirma se o utilizador foi encontrado
        if not user:
            raise HTTPException(status_code=404, detail="Erro ao encontar utilizador")

        # Verifica a password e o salt
        if verificar_password(user_login.password, user.password_hash, user.salt):
            # Gera o token JWT
            return generate_jwt_token_login(user.utilizador_ID, user.email, user.role )
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
    exp = None
    id_user = None
    token = None
    try:
        if await user_exists(db, email):
            id_user = get_user_by_email(db, email).utilizador_ID
            token, exp = generate_jwt_token_recovery(id_user, email)
            send_recovery_password_email(email, token)
        add_save_token(token, id_user, email, "recovery", exp)
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

async def eliminar_utilizador(db: Session, email: str):
    try:
        # Remove os espaços do email
        email_new= formatar_string(email)

        # Verifica se o email existe
        if not await user_exists(db, email_new):
            raise HTTPException(status_code=404, detail="Utilizador não existe.")

        # Vai a db buscar informações do utilizador
        user = get_user_by_email(db, email_new)

        # Confirma se o utilizador foi encontrado
        if not user:
            raise HTTPException(status_code=404, detail="Erro ao encontar utilizador")
        teste= apagar(db, user.utilizador_ID)

        return teste
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def atualizar_utilizador(db: Session, id: int,dados: UserUpdateInfo):
    try:
        return atualizar_utilizador_db(db, id,dados)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))