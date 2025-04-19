import datetime

from db.models import Utilizador
from httpx import AsyncClient
from main import app
from backend.tests.conftest import token_user

def test_registar_utilizador(client, db_session, token_admin):

    user_data = {
        "email": "newuser@gmail.com",
        "role": "residente"
    }

    response = client.post(
        "/api/registar",
        json=user_data,
        cookies={"access_token": token_admin}  # Passando o token no cookie
    )

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.json()}")  # Imprime o conteúdo da resposta para diagnóstico

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["message"] == "Registo realizado com sucesso"

    db_user = db_session.query(Utilizador).filter(Utilizador.Email == user_data["email"]).first()
    assert db_user is not None
    assert db_user.Email == user_data["email"]

async def test_verificacao_token_valido(client, db_session, token_admin,utilizador_registado):

    utilizador = utilizador_registado

    token = token_user(utilizador.UtilizadorID,utilizador.TipoUtilizador_.DescTU,utilizador.Email)

    response = client.get(
        "/api/verification/{token}",
        cookies={"access_token": token}  # Passando o token no cookie
    )

    # Debugando a resposta para verificar o que está sendo retornado
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.json()}")

    # Assert para verificar se a resposta foi bem-sucedida
    assert response.status_code == 200

    # Verificando o conteúdo da resposta
    response_data = response.json()
    assert response_data["message"] == "Verificação realizada com sucesso"  # Ajuste conforme sua resposta esperada

    # Verificando se o usuário foi encontrado na base de dados
    db_user = db_session.query(Utilizador).filter(Utilizador.Email == utilizador.Email).first()
    assert db_user is not None
    assert db_user.Email == utilizador.Email

    db_session.rollback()



