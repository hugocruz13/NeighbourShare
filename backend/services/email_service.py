import os
from fastapi import HTTPException

import resend

resend.api_key = os.getenv("RESEND_API_KEY")

URL = "http://127.0.0.1:8000"

def send_verification_email(user_email: str, token: str):
    """Envia um e-mail de verificação com um link contendo o token."""

    # Criar URL de verificação com o token
    verification_link = f"{URL}/api/verification/{token}"

    # Conteúdo do e-mail
    params: resend.Emails.SendParams = {
        "from": "NeighbourShare <no-reply@verification.igorcosta.pt>",
        "to": [user_email],
        "subject": "Confirmação de Conta",
        "html": f"""
            <p>Olá,</p>
            <p>Para concluir o seu registro, clique no link abaixo:</p>
            <p><a href="{verification_link}">{verification_link}</a></p>
        """,
    }
    try:
        email_response = resend.Emails.send(params)
        return email_response
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def send_recovery_password_email(user_email: str, token: str):
    """Envia um e-mail de recuperação do password com um link contendo o token."""

    # Criar URL de verificação com o token
    rec_link = f"{URL}/api/password/{token}"

    # Conteúdo do e-mail
    params: resend.Emails.SendParams = {
        "from": "NeighbourShare <no-reply@verification.igorcosta.pt>",
        "to": [user_email],
        "subject": "Recuperação de Password",
        "html": f"""
            <p>Olá,</p>
            <p>Clique no link abaixo para alterar a password</p>
            <p><a href="{rec_link}">{rec_link}</a></p>
        """,
    }
    try:
        email_response = resend.Emails.send(params)
        return email_response
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        raise HTTPException(status_code=500, detail=str(e))
