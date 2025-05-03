import pytest
from datetime import date, timedelta
import os
from typing import Dict, Any
from fastapi.testclient import TestClient
from main import app
from db.session import get_db

import os
os.environ["TESTING"] = "1"

class DataFlow:
    """Classe para armazenar dados de teste entre várias etapas"""
    def __init__(self):
        self.pedido_id = None
        self.votacao_id = None
        self.orcamento_votacao_id = None
        self.orcamentos_ids = []

@pytest.fixture(scope="module")
def data_flow():
    """Dados compartilhados entre testes"""
    return DataFlow()

@pytest.fixture
def db_session():
    """Cria uma sessão de banco de dados para teste"""
    db = next(get_db())
    yield db
    db.close()

@pytest.fixture
def client():
    """Cria um cliente de teste"""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def residente_token(client):
    """Obtém um token de autenticação de residente"""
    residente_login_data = {"email": "residente@email.com", "password": "residente"}
    response = client.post("/api/login", json=residente_login_data)
    assert response.status_code == 200, f"Login de residente falhou: {response.text}"
    return response.cookies.get("access_token")

@pytest.fixture
def gestor_token(client):
    """Obtém um token de autenticação de gestor"""
    gestor_login_data = {"email": "gestor@email.com", "password": "gestor"}
    response = client.post("/api/login", json=gestor_login_data)
    assert response.status_code == 200, f"Login de gestor falhou: {response.text}"
    return response.cookies.get("access_token")

@pytest.fixture
def test_pdf_path():
    """Cria um ficheiro PDF de teste para uploads"""
    pdf_path = "test_budget.pdf"
    with open(pdf_path, "w") as f:
        f.write("Conteúdo PDF de teste")
    yield pdf_path
    # Limpeza
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    
def test_01_criar_novo_pedido_recurso(client, residente_token, data_flow):
    """"Teste de criação de um novo pedido de recurso por um residente"""
    descricao = "Aquisição de mesa de ping-pong"
    client.cookies.set("access_token", residente_token)
    response = client.post(
        "/api/recursoscomuns/pedidosnovos/inserir",
        params={"desc_pedido_novo_recurso": descricao}
    )
    assert response.status_code == 200
    # Buscar o pedido criado
    client.cookies.set("access_token", residente_token)
    pedidos = client.get("/api/recursoscomuns/pedidosnovos").json()
    pedido = next((p for p in pedidos if p["DescPedidoNovoRecurso"] == descricao), None)
    assert pedido is not None
    data_flow.pedido_id = pedido["PedidoNovoRecID"]
    

def test_02_criar_nova_votacao(client, gestor_token, data_flow):
    """Teste de registro de votação pelo gestor para o pedido"""
    client.cookies.set("access_token", gestor_token)
    data_fim = (date.today() + timedelta(days=3)).isoformat()
    payload = {
        "titulo": "Aprovar aquisição?",
        "descricao": "Votação para aprovar aquisição do recurso.",
        "id_processo": data_flow.pedido_id,
        "data_fim": data_fim,
        "tipo_votacao": "Aquisição"
    }
    response = client.post("/api/criarvotacao", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert "id_votacao" in data
    data_flow.votacao_id = data["id_votacao"]


def test_03_simulacao_votos(client, gestor_token, data_flow):
    """Teste de simulação de votos de múltiplos residentes"""
    # Simula voto do gestor
    client.cookies.set("access_token", gestor_token)
    voto_payload = {"id_votacao": data_flow.votacao_id, "voto": "Sim"}
    response = client.post("/api/votar", json=voto_payload)
    assert response.status_code == 200
    # Simula voto de outro residente
    login_data = {"email": "residente@email.com", "password": "residente"}
    login_resp = client.post("/api/login", json=login_data)
    assert login_resp.status_code == 200
    token = login_resp.cookies.get("access_token")
    client.cookies.set("access_token", token)
    voto_payload = {"id_votacao": data_flow.votacao_id, "voto": "Sim"}
    response = client.post("/api/votar", json=voto_payload)
    assert response.status_code == 200


def test_04_processar_votos(client, gestor_token, data_flow):
    """Teste de processamento dos resultados da votação"""
    client.cookies.set("access_token", gestor_token)
    response = client.get(f"/api/terminar_votacao?votacao_id={data_flow.votacao_id}")
    print(response.json())
    assert response.status_code == 200
    # O resultado deve indicar aprovação
    data = response.json()
    
    assert "Sim" in str(data) or "aprovada" in str(data).lower()


def test_05_gestor_registra_orcamentos(client, gestor_token, data_flow, test_pdf_path):
    """Teste de registro de opções de orçamento pelo gestor"""
    client.cookies.set("access_token", gestor_token)
    # Buscar entidades externas
    entidades = client.get("/api/entidades/ver").json()
    assert entidades, "Necessário pelo menos uma entidade externa para orçamento."
    entidade_id = entidades[0]["EntidadeID"]
    # Primeira opção de orçamento
    with open(test_pdf_path, "rb") as f:
        files = {"pdforcamento": (test_pdf_path, f, "application/pdf")}
        data = {
            "id_entidade_externa": str(entidade_id),
            "valor_orcamento": "1000.00",
            "descricao_orcamento": "Orçamento 1",
            "idprocesso": str(data_flow.pedido_id),
            "tipoorcamento": "Aquisição"
        }
        response = client.post("/api/orcamentos/inserir", data=data, files=files)
        assert response.status_code == 200
    # Segunda opção de orçamento
    with open(test_pdf_path, "rb") as f:
        files = {"pdforcamento": (test_pdf_path, f, "application/pdf")}
        data = {
            "id_entidade_externa": str(entidade_id),
            "valor_orcamento": "1200.00",
            "descricao_orcamento": "Orçamento 2",
            "idprocesso": str(data_flow.pedido_id),
            "tipoorcamento": "Aquisição"
        }
        response = client.post("/api/orcamentos/inserir", data=data, files=files)
        assert response.status_code == 200
    # Guardar os IDs dos orçamentos
    orcamentos = client.get("/api/orcamentos/listar/").json()
    for orc in orcamentos:
        if orc["DescOrcamento"] in ["Orçamento 1", "Orçamento 2"]:
            data_flow.orcamentos_ids.append(orc["OrcamentoID"])


def test_06_gestor_cria_votacao_orcamentos(client, gestor_token, data_flow):
    """Teste de criação de votação para opções de orçamento pelo gestor"""
    client.cookies.set("access_token", gestor_token)
    data_fim = (date.today() + timedelta(days=2)).isoformat()
    payload = {
        "titulo": "Escolha do orçamento",
        "descricao": "Votação para escolher orçamento.",
        "id_processo": data_flow.pedido_id,
        "data_fim": data_fim,
        "tipo_votacao": "Aquisição"
    }
    response = client.post("/api/criarvotacao", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert "id_votacao" in data
    data_flow.orcamento_votacao_id = data["id_votacao"]


def test_07_simular_votos_orcamento(client, gestor_token, data_flow):
    """Teste de simulação de votos para opções de orçamento"""
    client.cookies.set("access_token", gestor_token)
    voto_payload = {"id_votacao": data_flow.orcamento_votacao_id, "voto": str(data_flow.orcamentos_ids[0])}
    response = client.post("/api/votar", json=voto_payload)
    assert response.status_code == 200
    # Simula voto de outro residente
    login_data = {"email": "residente@email.com", "password": "residente"}
    login_resp = client.post("/api/login", json=login_data)
    assert login_resp.status_code == 200
    token = login_resp.cookies.get("access_token")
    client.cookies.set("access_token", token)
    voto_payload = {"id_votacao": data_flow.orcamento_votacao_id, "voto": str(data_flow.orcamentos_ids[1])}
    response = client.post("/api/votar", json=voto_payload)
    assert response.status_code == 200
    

def test_08_processar_resultados_votacao_orcamento(client, gestor_token, data_flow):
    """Teste de processamento dos resultados da votação de orçamento"""
    client.cookies.set("access_token", gestor_token)
    response = client.get(f"/api/terminar_votacao?votacao_id={data_flow.orcamento_votacao_id}")
    assert response.status_code == 200
    data = response.json()
    # O resultado deve indicar um orçamento vencedor
    assert any(str(orc_id) in str(data) for orc_id in data_flow.orcamentos_ids)



def test_09_verificao_estado_final_pedido(client, gestor_token, data_flow):
    """Teste de verificação do estado final do pedido de recurso"""
    client.cookies.set("access_token", gestor_token)
    pedidos = client.get("/api/recursoscomuns/pedidosnovos").json()
    pedido = next((p for p in pedidos if p["PedidoNovoRecID"] == data_flow.pedido_id), None)
    assert pedido is not None
    # O estado deve refletir aprovação e orçamento escolhido
    #assert "Aprovado" in pedido["EstadoPedidoNovoRecurso_"]["DescEstadoPedidoNovoRecurso"] or "Orçamento" in pedido["EstadoPedidoNovoRecurso_"]["DescEstadoPedidoNovoRecurso"]