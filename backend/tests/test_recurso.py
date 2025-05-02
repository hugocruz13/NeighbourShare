import pytest
from fastapi.testclient import TestClient
import decimal
from db.models import Recurso
from main import app
from db.session import get_db
import os

import os
os.environ["TESTING"] = "1"

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def db_session():
    db = next(get_db())
    yield db

@pytest.fixture
def cookie_residente(client):
    login_data = {
        "email": "residente@email.com",
        "password": "residente"
    }
    response = client.post("/api/login", json=login_data)
    assert response.status_code == 200
    token = response.cookies.get("access_token")
    assert token is not None

    return response.cookies

@pytest.fixture
def cookie_gestor(client):
    login_data = {
        "email": "gestor@email.com",
        "password": "gestor"
    }
    response = client.post("/api/login", json=login_data)
    assert response.status_code == 200
    token = response.cookies.get("access_token")
    assert token is not None
    return response.cookies

@pytest.fixture
def cookie_admin(client):
    login_data = {
        "email": "admin@email.com",
        "password": "admin"
    }
    response = client.post("/api/login", json=login_data)
    assert response.status_code == 200

    token = response.cookies.get("access_token")
    assert token is not None

    return response.cookies

@pytest.fixture
def resource_data(db_session):
    novo_recurso = Recurso(
        Nome="Guarda-Sol Teste fixture",
        DescRecurso="Guarda-Sol médido, pode ser usado na praia ou outras áreas de lazer",
        Caucao=decimal.Decimal(20.0),
        UtilizadorID=2,
        DispID=1,
        CatID=1,
        Path="none"
    )
    db_session.add(novo_recurso)
    db_session.commit()
    db_session.refresh(novo_recurso)

    return novo_recurso.RecursoID

def test_01_registar_recurso(client, db_session, cookie_residente):
    """Um utilizador pode registar um novo recurso"""
    # Caminho para a imagem
    caminho_imagem = "gs.jpg"
    client.cookies.set("access_token", cookie_residente.get("access_token"))

    # Dados do formulário (campos de texto)
    dados_formulario = {
        "nome_recurso": "Guarda-Sol Teste",
        "descricao_recurso": "Guarda-Sol médido, pode ser usado na praia ou outras áreas de lazer",
        "caucao_recurso": 20.0,
        "recurso_disponivel": "Disponível",
        "categoria_recurso": "Lazer",
    }

    # Preparar o arquivo para envio
    ficheiros = {
        "fotos_recurso": (os.path.basename(caminho_imagem), open(caminho_imagem, "rb"), "image/jpeg")
    }

    response = client.post(
        "/api/recursos/inserir",
        data=dados_formulario,
        files=ficheiros
    )

    assert response.status_code == 200
    recur = db_session.query(Recurso).filter(Recurso.Nome == "Guarda-Sol Teste").first()
    assert recur is not None


def test_02_listar_recursos(client, cookie_residente):
    """Um utilizador ver os recursos registados"""
    client.cookies.set("access_token", cookie_residente.get("access_token"))

    response = client.get("/api/recursos/")
    assert response.status_code == 200
    recursos = response.json()

    chaves_obrigatorias = {
        "RecursoID",
        "Nome",
        "DescRecurso",
        "Caucao",
        "Categoria_",
        "Utilizador_",
        "Disponibilidade_",
        "Image"
    }

    chaves_categoria = {"CatID", "DescCategoria"}
    chaves_utilizador = {"UtilizadorID", "NomeUtilizador"}
    chaves_disponibilidade = {"DispID", "DescDisponibilidade"}

    for recurso in recursos:
        # Verifica se todas as chaves principais existem
        assert chaves_obrigatorias.issubset(recurso.keys()), f"Recurso incompleto: {recurso}"

        # Verifica subestruturas
        assert chaves_categoria.issubset(recurso["Categoria_"].keys()), f"Categoria incompleta: {recurso['Categoria_']}"
        assert chaves_utilizador.issubset(
            recurso["Utilizador_"].keys()), f"Utilizador incompleto: {recurso['Utilizador_']}"
        assert chaves_disponibilidade.issubset(
            recurso["Disponibilidade_"].keys()), f"Disponibilidade incompleta: {recurso['Disponibilidade_']}"

def test_03_ver_recurso(client, cookie_residente, resource_data):
    """Um utilizador pode ver um recurso"""
    client.cookies.set("access_token", cookie_residente.get("access_token"))

    response = client.get(f"/api/recursos/{resource_data}")

    assert response.status_code == 200
    responde_data = response.json()
    assert responde_data["Nome"] == "Guarda-Sol Teste fixture"