import pytest
from datetime import date, timedelta
import os
from fastapi.testclient import TestClient
from main import app
from db.session import get_db
from db.models import RecursoComun, PedidoManutencao

import os
os.environ["TESTING"] = "1"

class DataFlow:
    """Classe para armazenar dados de teste entre várias etapas"""
    def __init__(self):
        self.pedido_id = None
        self.votacao_id = None
        self.orcamento_votacao_id = None
        self.orcamentos_ids = []
        self.recursocomum_id = None

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

@pytest.fixture
def test_image_path():
    """Cria um ficheiro PNG de teste para upload"""
    png_path = "imagem.png"
    with open(png_path, "w") as f:
        f.write("a")
    yield png_path
    if os.path.exists(png_path):
        os.remove(png_path)

@pytest.fixture
def inserir_recurso_comun(db_session, client, gestor_token, test_image_path, data_flow):
    client.cookies.set("access_token", gestor_token)
    with open(test_image_path, "rb") as f:
        files = {"imagem": (test_image_path, f, "image/png")}
        data = {
                "nome_recurso": "Elevador Teste",
                "descricao_recurso": "Elevador central do condomínio"
        }
        response = client.post("/api/recursoscomuns/inserir", data=data, files=files)
        assert response.status_code == 200
    recurso = db_session.query(RecursoComun).filter(RecursoComun.Nome == "Elevador Teste").order_by(RecursoComun.RecComumID.desc()).first()
    assert recurso is not None
    data_flow.recursocomum_id = recurso.RecComumID
    return recurso.RecComumID

def test_01_criar_um_novo_pedido_manutencao(db_session, client, residente_token, data_flow, inserir_recurso_comun):
    """Teste da criação de um novo pedido de manutenção por um residente"""
    client.cookies.set("access_token", residente_token)
    payload = {
        "recurso_comum_id": inserir_recurso_comun,
        "desc_manutencao_recurso_comum": "Elevador avariou por causa do apagão"
    }
    response = client.post("/api/recursoscomuns/pedidosmanutencao/inserir", json=payload)
    assert response.status_code == 200
    pedido_manutencao = db_session.query(PedidoManutencao).filter(PedidoManutencao.RecComumID == data_flow.recursocomum_id).first()
    assert pedido_manutencao is not None
    data_flow.pedido_id=pedido_manutencao.PMID


def test_02_gestor_verifica_pedido_manutencao(db_session, client, gestor_token, data_flow):
    """O gestor irá verificar a necessidade do pedido de manutenção e se é necessário mão externa"""
    client.cookies.set("access_token", gestor_token)
    response = client.get("/api/recursoscomuns/pedidosmanutencao/estados")
    assert response.status_code == 200
    response_data = response.json()
    result = next((item for item in response_data if item['DescEstadoPedidoManutencao'] == "Aprovado para execução externa"), None)
    id_num = result["EstadoPedManuID"]
    assert id_num is not None
    payload = {
        "novo_estado_id": str(id_num)
    }
    response = client.put(f"/api/recursoscomuns/pedidosmanutencao/{data_flow.pedido_id}/estado", json=payload)
    print(response.json())
    assert response.status_code == 200
    pedido = db_session.query(PedidoManutencao).filter(PedidoManutencao.PMID == data_flow.pedido_id).first()
    assert pedido.EstadoPedManuID == id_num

def test_03_registar_orcamento_manutencao(client, gestor_token, data_flow, test_pdf_path):
    """O gestor irá registar o orçamento dado pela entidade externa"""
    client.cookies.set("access_token", gestor_token)
    # Buscar entidades externas
    entidades = client.get("/api/entidades/ver").json()
    assert entidades, "Necessário pelo menos uma entidade externa para orçamento."
    entidade_id = entidades[0]["EntidadeID"]
    with open(test_pdf_path, "rb") as f:
        files = {"pdforcamento": (test_pdf_path, f, "application/pdf")}
        data = {
            "id_entidade_externa": str(entidade_id),
            "valor_orcamento": "1000.00",
            "descricao_orcamento": "Orçamento manutenção teste",
            "idprocesso": str(data_flow.pedido_id),
            "tipoorcamento": "Manutenção"
        }
        response = client.post("/api/orcamentos/inserir", data=data, files=files)
        assert response.status_code == 200
    # Guardar o id do orçamento
    orcamentos = client.get("/api/orcamentos/listar/").json()
    orcamento = next((o for o in orcamentos if o["DescOrcamento"] == "Orçamento manutenção teste"), None)
    assert orcamento is not None
    data_flow.orcamentos_ids = [orcamento["OrcamentoID"]]

def test_04_criar_votacao(client, gestor_token, data_flow):
    """O gestor irá criar uma votação para votar no orçamento da manutenção"""
    client.cookies.set("access_token", gestor_token)
    from datetime import date, timedelta
    data_fim = (date.today() + timedelta(days=2)).isoformat()
    payload = {
        "titulo": "Escolha do orçamento manutenção",
        "descricao": "Votação para escolher orçamento de manutenção.",
        "id_processo": data_flow.pedido_id,
        "data_fim": data_fim,
        "tipo_votacao": "Manutenção"
    }
    response = client.post("/api/criarvotacao", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert "id_votacao" in data
    data_flow.votacao_id = data["id_votacao"]

def test_05_simular_votos(client, residente_token, gestor_token, data_flow):
    """Teste de simulação de votos de múltiplos residentes"""
    client.cookies.set("access_token", residente_token)
    voto_payload = {"id_votacao": data_flow.votacao_id, "voto": str(data_flow.orcamentos_ids[0])}
    response = client.post("/api/votar", json=voto_payload)
    assert response.status_code == 200
    # Simula voto do gestor
    client.cookies.set("access_token", gestor_token)
    response = client.post("/api/votar", json=voto_payload)
    assert response.status_code == 200

def test_06_terminar_votacao(client, gestor_token, data_flow):
    """Terminar a votacao e verificar o resultado"""
    client.cookies.set("access_token", gestor_token)
    response = client.get(f"/api/terminar_votacao?votacao_id={data_flow.votacao_id}")
    assert response.status_code == 200
    data = response.json()
    assert str(data_flow.orcamentos_ids[0]) in str(data)

def test_07_registar_manutencao(client, gestor_token, data_flow):
    """Teste de introdução dos detalhes da manutenção"""
    client.cookies.set("access_token", gestor_token)
    # Buscar orçamento escolhido
    orcamento_id = data_flow.orcamentos_ids[0]
    payload = {
        "PMID": data_flow.pedido_id,
        "DataManutencao": "2025-05-02",
        "DescManutencao": "Manutenção do elevador",
        "Orcamento_id": orcamento_id
    }
    response = client.post("/api/recursoscomuns/manutencao/inserir", json=payload)
    print(response.json())
    assert response.status_code == 200

def test_08_terminar_manutencao(client, gestor_token, data_flow):
    """Dar por terminada a manutencao do recurso comun"""
    client.cookies.set("access_token", gestor_token)
    # Buscar manutenção criada
    manutencoes = client.get("/api/recursoscomuns/manutencao/").json()
    manutencao = next((m for m in manutencoes if m["PMID"] == data_flow.pedido_id), None)
    assert manutencao is not None
    manutencao_id = manutencao["ManutencaoID"]
    response = client.get("/api/recursoscomuns/manutencao/estados")
    response_data = response.json()
    assert response.status_code == 200
    result = next((item for item in response_data if item['DescEstadoManutencao'] == "Concluído"), None)
    payload = {"novo_estado_id": str(result["EstadoManuID"])}
    response = client.put(f"/api/recursoscomuns/manutencao/update/{manutencao_id}/estado", json=payload)
    print(response.json())
    assert response.status_code == 200