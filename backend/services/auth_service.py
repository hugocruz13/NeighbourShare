import os
import time
from typing import reveal_type

from db.repository.user_repo import *
from schemas.user_schemas import UserJWT, UserLogin, ResetPassword, UserUpdateInfo, ChangeRole
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from db.repository.user_repo import get_id_role, create_user, user_exists, get_user_by_email, apagar, atualizar_utilizador_db
from utils.PasswordHasher import hash_password, verificar_password
from services.jwt_services import generate_jwt_token_login, generate_jwt_token_registo, generate_jwt_token_recovery
from services.email_service import send_verification_email, send_recovery_password_email
from utils.tokens_record import add_save_token, revoke_token, save_tokens_record_list_login
from utils.string_utils import formatar_string


async def get_user_data(db: Session, id_user:int):
    try:
        return await get_dados_utilizador(db, id_user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def atualizar_novo_utilizador(user: NewUserUpdate, imagem:UploadFile,token:UserJWT, db: Session):
    try:
        if await user_exists(db, str(token.email)):
            password_hashed, salt = hash_password(user.password)
            path = await guardar_imagem(imagem, token.id)
            user.path = path
            await update_new_user(db, user, token.id, password_hashed, salt,path)
            user.password = ""
            return True, "Utilizador atualizado com sucesso"
        else:
            return False, "Erro ao verificar utilizador"
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def guardar_imagem(imagem:UploadFile, user_id:int):
    try:
        tipos_permitidos = ['image/png', 'image/jpeg', 'image/jpg']

        if imagem.content_type not in tipos_permitidos:
            raise HTTPException (status_code=400, detail="Apenas imagens são permitidas (png, jpeg, jpg)")

        pasta_imagens = os.getenv('UPLOAD_DIR_PERFIL')

        imagem_path = os.path.join(pasta_imagens, str(user_id))

        os.makedirs(imagem_path, exist_ok=True)

        caminho_arquivo = os.path.join(imagem_path, imagem.filename)
        with open(caminho_arquivo,'wb+') as f:
            f.write(imagem.file.read())

        url_imagens = os.getenv('SAVE_PERFIL')
        path = os.path.join(url_imagens,str(user_id), imagem.filename)
        clean_path = path.replace("\\", "/")
        return clean_path
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
            token = generate_jwt_token_login(user.utilizador_ID, user.email, user.role )
            save_tokens_record_list_login(user.utilizador_ID, token, user.role)
            return token
        else:
            raise HTTPException(status_code=401, detail="Password incorreta")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def verificao_utilizador(db: Session, user: UserJWT):
    try:
        return await user_exists(db, user.email)
    except HTTPException as e:
        raise e
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
    except HTTPException as e:
        raise e
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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

##atualiza o utilizador
async def atualizar_utilizador(db: Session, id: int,dados: UserUpdateInfo):
    try:
        return atualizar_utilizador_db(db, id,dados)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def mudar_role(dados: ChangeRole, user: UserJWT, db: Session):
    utilizador = await get_utilizador_por_id(dados.id, db)
    role_id = await get_id_role(db, dados.role)
    if role_id is None:
        raise HTTPException(status_code=400, detail="Cargo inserido inválido")
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    try:
        await atualizar_role_utilizador(utilizador, role_id, db)
        revoke_token(None, dados.id, time.time())
        return True
    except HTTPException as e:
        raise e


