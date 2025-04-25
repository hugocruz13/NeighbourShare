import time

import db
from middleware.auth_middleware import verify_token_login, verify_token_verification
from main import app
from fastapi.testclient import TestClient
from db.models import Utilizador
import pytest
from tests.test_email_config import testemail
from uuid import uuid4
import json

class DataFlow:
    def __init__(self):
        self.id_user = None
        self.verification_token = None
        self.access_token = None
        self.recovery_token = None
        self.email = None

@pytest.fixture(scope="module")  # or "session" if you want it across multiple test files
def data_flow():
    return DataFlow()

@pytest.fixture
def test_email(testemail):
    """Generate a unique test email address"""
    unique_id = uuid4().hex[:8]
    return f"{testemail.namespace}.{unique_id}@inbox.testmail.app"

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def admin_data(db_session):
    user_data = {
        "email": "admin@email.com",
        "password": "admin"
    }
    assert db_session.query(Utilizador).filter(Utilizador.Email == user_data["email"]).first() is not None
    return user_data

@pytest.fixture
def user_data():
    return {
        "nome": "string",
        "data_nascimento": "2025-04-24",
        "contacto": 182934812,
        "password": "98Paulosss#@"
    }

@pytest.fixture
def test_user_data(test_email):
    return {
        "email": test_email,
        "role": "residente"
    }

@pytest.fixture
def token_admin(client, admin_data):
    """Um administrador pode fazer login com sucesso"""
    response = client.post("/api/login", json=admin_data)
    assert response.status_code == 200
    print("Login response:", response.json())
    return response.cookies.get("access_token")

def test_01_login_admin(client, admin_data):
    """Um administrador pode fazer login com sucesso"""
    response = client.post("/api/login", json=admin_data)
    assert response.status_code == 200
    print("Login response:", response.json())

    # Extrai o cookie manualmente (porque o TestClient não o está a guardar automaticamente)
    access_token = response.cookies.get("access_token")
    assert access_token is not None, "Cookie access_token não recebido"
    assert verify_token_login(access_token)

    client.cookies.set("access_token", access_token)

    response = client.get("/api/me")
    print("Status:", response.status_code)
    print("Data:", response.json())
    assert response.status_code == 200
    assert response.json()["role"] == "admin"

async def test_02_new_user(client, token_admin, db_session, test_user_data, testemail, data_flow):

    """Um administrador pode registar um novo utilizador residente"""
    client.cookies.set("access_token", token_admin)

    response = client.post(
        "/api/registar",
        json=test_user_data
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Registo realizado com sucesso"
    data_flow.email = test_user_data["email"]
    # Verify user exists in database
    db_user = db_session.query(Utilizador).filter(Utilizador.Email == test_user_data["email"]).first()
    assert db_user is not None
    assert db_user.Email == test_user_data["email"]
    assert db_user.Verificado is False

    used = extract_used_json("tokens.json", test_user_data["email"])
    assert used is not None
    assert used is False

    time.sleep(3)
    message = await testemail.get_message()
    token = testemail.extract_verification_token_from_email(message, test_user_data["email"])
    assert token is not None
    assert verify_token_verification(token)
    print(f"Token extracted: {token}")
    assert verify_token_verification(token)

    # Store token for next test
    data_flow.verification_token = token
    data_flow.id_user = db_user.UtilizadorID

def test_03_update_new_user(client, db_session, data_flow, test_user_data):
    response = client.get(
        f"/api/verification/{data_flow.verification_token}",
    )

    #assert response.status_code == 307
    #url = response.headers.get("location")
    #response = client.get(
    #    url
    #)
    assert response.status_code == 200

    user_data = {
        "nome": "string",
        "data_nascimento": "2025-04-24",
        "contacto": 182934812,
        "password": "98Paulosss#@"
    }
    response = client.post(
        f"/api/registar/atualizar_dados",
        json=user_data,
        params={"token": data_flow.verification_token}
    )

    assert response.status_code == 200
    response_data = response.json()
    #assert response_data[0] == "Dados atualizados com sucesso."

    assert db_session.query(Utilizador).filter(Utilizador.UtilizadorID == data_flow.id_user).first().NomeUtilizador == user_data["nome"]
    assert db_session.query(Utilizador).filter(Utilizador.UtilizadorID == data_flow.id_user).first().Contacto == user_data["contacto"]
    assert db_session.query(Utilizador).filter(Utilizador.UtilizadorID == data_flow.id_user).first().Verificado is True

    used = extract_used_json("tokens.json", test_user_data["email"])
    assert used is None

def test_04_view_profile(client, db_session, data_flow, user_data, test_user_data):
    """Um utilizador registado pode fazer login com sucesso"""
    login_info = {
        "email": data_flow.email,
        "password": "98Paulosss#@"
    }
    response = client.post("/api/login", json=login_info)
    assert response.status_code == 200
    print("Login response:", response.json())
    access_token = response.cookies.get("access_token")
    client.cookies.set("access_token", access_token)

    response = client.get(
        "/api/perfil"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("nome") == user_data["nome"]
    assert response_data.get("contacto") == user_data["contacto"]
    assert response_data.get("email") == data_flow.email

def extract_used_json(file_path, target_email):
    try:
        # Read and parse the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Search for the target email
        for entry in data:
            if entry.get('email') == target_email:
                return entry.get('used')

        # Email not found
        print(f"Email '{target_email}' not found in the JSON data.")
        return None

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
