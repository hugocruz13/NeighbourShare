from io import BytesIO
from unittest.mock import AsyncMock
import pytest
from fastapi import UploadFile, HTTPException
from db.session import get_db
from schemas.orcamento_schema import OrcamentoSchema, TipoOrcamento, OrcamentoUpdateSchema
from services.orcamento_service import inserir_orcamento_service, listar_orcamentos_service, eliminar_orcamento_service, \
    alterar_orcamento_service


#Coneção com a base de dados
@pytest.fixture
def db_session():
    db = next(get_db())
    yield db

async def test_inserir_orcamento_service_Manutencao(db_session):
    #Arrange
    orcamento = OrcamentoSchema(IDEntidade=3, Valor=100,DescOrcamento="Teste",NomePDF="Teste",IDProcesso=2, TipoProcesso=TipoOrcamento.MANUTENCAO)
    fake_pdf = AsyncMock(spec=UploadFile)
    fake_pdf.filename = "teste.pdf"
    fake_pdf.file = BytesIO(b"conteudo de teste")
    fake_pdf.content_type = "application/pdf"

    #Act
    result = await inserir_orcamento_service(db_session, orcamento,fake_pdf)

    #Assert
    assert result[0] == True
    assert result[1] == {'message': 'Inserção feita com sucesso'}

async def test_inserir_orcamento_service_Manutencao_erro(db_session):
    #Arrange (Pedido de manutenção não existe)
    orcamento = OrcamentoSchema(IDEntidade=3, Valor=100,DescOrcamento="Teste",NomePDF="Teste",IDProcesso=6, TipoProcesso=TipoOrcamento.MANUTENCAO)
    fake_pdf = AsyncMock(spec=UploadFile)
    fake_pdf.filename = "teste.pdf"
    fake_pdf.file = BytesIO(b"conteudo de teste")
    fake_pdf.content_type = "application/pdf"

    #Act
    result = await inserir_orcamento_service(db_session, orcamento,fake_pdf)

    #Assert
    assert result[0] == False
    assert result[1] == {'message': 'Erro ao encontrar o pedido de manutenção!'}


async def test_inserir_orcamento_service_Aquisicao(db_session):
    #Arrange
    orcamento = OrcamentoSchema(IDEntidade=3, Valor=100,DescOrcamento="Teste",NomePDF="Teste",IDProcesso=1, TipoProcesso=TipoOrcamento.AQUISICAO)
    fake_pdf = AsyncMock(spec=UploadFile)
    fake_pdf.filename = "teste"
    fake_pdf.file = BytesIO(b"conteudo de teste")
    fake_pdf.content_type = "application/pdf"

    #Act
    result = await inserir_orcamento_service(db_session, orcamento,fake_pdf)

    #Assert
    assert result[0] == True
    assert result[1] == {'message': 'Inserção feita com sucesso'}

async def test_inserir_orcamento_service_Aquisicao_erro(db_session):
    #Arrange (Entidade não existe)
    orcamento = OrcamentoSchema(IDEntidade=15, Valor=100,DescOrcamento="Teste",NomePDF="Teste",IDProcesso=1, TipoProcesso=TipoOrcamento.MANUTENCAO)
    fake_pdf = AsyncMock(spec=UploadFile)
    fake_pdf.filename = "teste"
    fake_pdf.file = BytesIO(b"conteudo de teste")
    fake_pdf.content_type = "application/pdf"

    #Act
    with pytest.raises(HTTPException) as exc_info:
        await inserir_orcamento_service(db_session, orcamento,fake_pdf)

    #Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Entidade Externa não registada"

async def test_listar_orcamentos_service(db_session):
    #Act
    lista = await listar_orcamentos_service(db_session)

    #Assert
    assert isinstance(lista, list)

async def test_eliminar_orcamento_service(db_session):
    # Arrange
    id_orcamento = 7

    # Act
    with pytest.raises(HTTPException) as exc_info:
        await eliminar_orcamento_service(db_session, id_orcamento)

    # Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Erro ao encontrar o caminho"

async def test_eliminar_orcamento_service_erro(db_session):
    # Arrange
    id_orcamento = 13

    # Act
    result = await eliminar_orcamento_service(db_session, id_orcamento)

    # Assert
    assert result[0] == False
    assert result[1] == {'erro': 'Orçamento não encontrado'}

async def test_alterar_orcamento_service(db_session):
    #Arrange
    orcamento = OrcamentoUpdateSchema(OrcamentoID=7,IDEntidade=10,Valor=260,DescOrcamento="teste")
    fake_pdf = AsyncMock(spec=UploadFile)
    fake_pdf.filename = "teste"
    fake_pdf.file = BytesIO(b"conteudo de teste")
    fake_pdf.content_type = "application/pdf"

    #Act
    with pytest.raises(HTTPException) as exc_info:
        await alterar_orcamento_service(db_session, orcamento,fake_pdf)

    #Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Orçamento não registado!"
