import os
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from db.session import get_db
from middleware.auth_middleware import role_required, verify_token_verification, verify_token_recuperacao
from schemas.user_schemas import UserRegistar, UserLogin, UserJWT, NewUserUpdate, ResetPassword, ForgotPassword
from services.auth_service import registar_utilizador, user_auth, atualizar_novo_utilizador, verificar_forgot, \
    verificao_utilizador, atualizar_nova_password, eliminar_utilizador
from fastapi.responses import RedirectResponse
from utils.tokens_record import validate_token_entry, mark_token_as_used
# Define o tempo do token
EXPIRE_MINUTES_LOGIN = int(os.getenv("EXPIRE_MINUTES_LOGIN"))

router = APIRouter(tags=['Autenticação'])

#Controler login, protegido
@router.post("/registar")
async def registar(user: UserRegistar, token: UserJWT = Depends(role_required(["admin"])), db: Session = Depends(get_db)):
    try:
        sucesso, mensagem = await registar_utilizador(user, db)
        if sucesso:
            return {"message": "Registo realizado com sucesso"}
        else:
            raise HTTPException(status_code=400, detail=mensagem)  # Erro
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail= {str(e)})

# Controller login
@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db), response: Response = Response):
    try:
        token = await user_auth(db, user)

        # Define o cookie de login
        response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,  # Impede acesso via JavaScript
                secure=True,  # Garante que o cookie seja enviado apenas por HTTPS
                samesite="strict",  # Controle de onde o cookie é enviado (Lax ou Strict)
                expires=datetime.now(timezone.utc) + timedelta(minutes=int(EXPIRE_MINUTES_LOGIN)),  # Expiração
        )
        return {"message": "Login com sucesso"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.get("/verification/{token}")
async def verificacao(token, db:Session = Depends(get_db)):
    try:
        b, message = validate_token_entry(token)
        if b is False:
            raise HTTPException(status_code=403, detail=message)
        payload = verify_token_verification(token)
        user = UserJWT(id=payload["id"], email=payload["email"], role=payload["role"])
        if await verificao_utilizador(db, user):
            # Redirecionar para página de atualizar dados para completar registo
            return RedirectResponse(url=f"http://127.0.0.1:8000/docs#/default/registar_atualizar_dados_api_registar_atualizar_dados_post?{token}") #TODO ALTERAR A URL
        else:
            raise HTTPException(status_code=400, detail="Token de verificação de email inválido")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.post("/registar/atualizar_dados")
async def registar_atualizar_dados(user: NewUserUpdate, token: str, db: Session = Depends(get_db)):
    try:
        b, message = validate_token_entry(token)
        if b is False:
            raise HTTPException(status_code=403, detail=message)
        payload = verify_token_verification(token)
        user_jwt = UserJWT(id=payload["id"], email=payload["email"], role=payload["role"])
        a, message = await atualizar_novo_utilizador(user, user_jwt, db)
        if a is True:
            mark_token_as_used(token)
        return a, message
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.post("/password/forgot")
async def esqueceu_password(user:ForgotPassword, db: Session = Depends(get_db)):
    try:
        return await verificar_forgot(db, str(user.email))
    except HTTPException as e:
        raise e

@router.get("/password/{token}")
async def recuperar_password(token, db: Session = Depends(get_db)):
    try:
        b, message = validate_token_entry(token)
        if b is False:
            raise HTTPException(status_code=403, detail=message)
        payload = verify_token_recuperacao(token)
        user = UserJWT(id=payload["id"], email=payload["email"], role="")
        if await verificao_utilizador(db, token):
            # Redirecionar para página de atualizar dados para completar registo
            return RedirectResponse(
                url=f"http://127.0.0.1:8000?{token}")  # TODO ALTERAR A URL
        else:
            raise HTTPException(status_code=400, detail="Token de recuperação password inválido")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.post("/password/reset")
async def resetar_password(senha: ResetPassword, token: str, db: Session = Depends(get_db)):
    try:
        b, message = validate_token_entry(token)
        if b is False:
            raise HTTPException(status_code=403, detail=message)
        payload = verify_token_recuperacao(token)
        user_jwt = UserJWT(id=payload["id"], email=payload["email"], role="")
        a, message = await atualizar_nova_password(db, senha, user_jwt)
        if a is True:
            mark_token_as_used(token)
        return a, message
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.get("/me")
async def about_me(user: UserJWT = Depends(role_required(["admin","residente","gestor"]))):
    try:
        return {"id": user.id, "email": user.email, "role": user.role}
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.delete("/delete")
async def delete_user(email:str,user: UserJWT = Depends(role_required(["admin"])), db: Session = Depends(get_db)):
    try:
        if await eliminar_utilizador(db, email):
            return {"message": "Utilizador eliminado com sucesso."}
        else:
            return {"message": "Erro ao eliminar utilizador."}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})