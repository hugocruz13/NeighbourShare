from io import BytesIO
from unittest.mock import AsyncMock
import pytest
from fastapi import UploadFile, HTTPException
from datetime import date
from db.models import EntidadeExterna, PedidoManutencao, RecursoComun, PedidoNovoRecurso
from db.repository.entidade_repo import inserir_entidade_testes
from db.repository.orcamento_repo import get_last_id
from db.repository.recurso_comum_repo import inserir_pedido_manutencao_test, inserir_recurso_comum_teste, \
    inserir_pedido_novo_recurso_teste
from db.session import get_db
from schemas.orcamento_schema import OrcamentoSchema, TipoOrcamento, OrcamentoUpdateSchema
from schemas.recurso_comum_schema import PedidoNovoRecursoSchemaCreate
from services.orcamento_service import inserir_orcamento_service, listar_orcamentos_service, eliminar_orcamento_service, \
    alterar_orcamento_service


#Coneção com a base de dados
@pytest.fixture
def db_session():
    db = next(get_db())
    yield db

async def test_inserir_orcamento_service_Manutencao(db_session):
    #Arrange
    entidade = await inserir_entidade_testes(db_session, EntidadeExterna(Especialidade="Elevadores",Contacto=253682023,Email="elevadores@teste.com",Nome="elevadores",Nif=123456789))
    recurso_comum= await inserir_recurso_comum_teste(db_session, RecursoComun(Nome="Elevador",DescRecursoComum="Testar",Path="none"))
    pedido_manutencao= await inserir_pedido_manutencao_test(db_session,PedidoManutencao(DescPedido="Teste",DataPedido=date.today(),RecComumID=recurso_comum.RecComumID,UtilizadorID=1,EstadoPedManuID=1))
    orcamento = OrcamentoSchema(IDEntidade=entidade.EntidadeID, Valor=100,DescOrcamento="Teste",NomePDF="Teste",IDProcesso=pedido_manutencao.EstadoPedManuID, TipoProcesso=TipoOrcamento.MANUTENCAO)
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
    orcamento = OrcamentoSchema(IDEntidade=3, Valor=100,DescOrcamento="Teste",NomePDF="Teste",IDProcesso=999, TipoProcesso=TipoOrcamento.MANUTENCAO)
    fake_pdf = AsyncMock(spec=UploadFile)
    fake_pdf.filename = "teste.pdf"
    fake_pdf.file = BytesIO(b"conteudo de teste")
    fake_pdf.content_type = "application/pdf"

    #Act
    with pytest.raises(HTTPException) as exc_info:
        await inserir_orcamento_service(db_session, orcamento,fake_pdf)

    #Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Pedido de mantenção não existe"


async def test_inserir_orcamento_service_Aquisicao(db_session):
    #Arrange
    entidade = await inserir_entidade_testes(db_session, EntidadeExterna(Especialidade="Elevadores", Contacto=253682023,Email="elevadores@teste.com",Nome="elevadores", Nif=123456789))
    pedido_aquisicao = await inserir_pedido_novo_recurso_teste(db_session,PedidoNovoRecurso(DescPedidoNovoRecurso="Quero um elevador novo",DataPedido=date.today(),UtilizadorID=1,EstadoPedNovoRecID=1))
    orcamento = OrcamentoSchema(IDEntidade=entidade.EntidadeID, Valor=100,DescOrcamento="Teste",NomePDF="Teste",IDProcesso=pedido_aquisicao.PedidoNovoRecID, TipoProcesso=TipoOrcamento.AQUISICAO)
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
    orcamento = OrcamentoSchema(IDEntidade=999, Valor=100,DescOrcamento="Teste",NomePDF="Teste",IDProcesso=1, TipoProcesso=TipoOrcamento.MANUTENCAO)
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
    entidade = await inserir_entidade_testes(db_session, EntidadeExterna(Especialidade="Elevadores", Contacto=253682023,Email="elevadores@teste.com",Nome="elevadores", Nif=123456789))
    pedido_aquisicao = await inserir_pedido_novo_recurso_teste(db_session,PedidoNovoRecurso(DescPedidoNovoRecurso="Quero um elevador novo",DataPedido=date.today(),UtilizadorID=1,EstadoPedNovoRecID=1))
    orcamento = OrcamentoSchema(IDEntidade=entidade.EntidadeID, Valor=100,DescOrcamento="Teste",NomePDF="Teste",IDProcesso=pedido_aquisicao.PedidoNovoRecID, TipoProcesso=TipoOrcamento.AQUISICAO)
    fake_pdf = AsyncMock(spec=UploadFile)
    fake_pdf.filename = "teste.pdf"
    fake_pdf.file = BytesIO(b"conteudo de teste")
    fake_pdf.content_type = "application/pdf"
    result = await inserir_orcamento_service(db_session, orcamento, fake_pdf)
    id_orcamento = await get_last_id(db_session)

    # Act
    result_final= await eliminar_orcamento_service(db_session,id_orcamento.OrcamentoID)

    # Assert
    result_final[0]==True
    result_final[1]=={'Orcamento removido com sucesso!'}


async def test_eliminar_orcamento_service_erro(db_session):
    # Arrange
    id_orcamento = 999

    # Act
    result = await eliminar_orcamento_service(db_session, id_orcamento)

    # Assert
    assert result[0] == False
    assert result[1] == {'erro': 'Orçamento não encontrado'}

async def test_alterar_orcamento_service(db_session):
    #Arrange
    entidade = await inserir_entidade_testes(db_session, EntidadeExterna(Especialidade="Elevadores", Contacto=253682023,Email="elevadores@teste.com",Nome="elevadores", Nif=123456789))
    pedido_aquisicao = await inserir_pedido_novo_recurso_teste(db_session,PedidoNovoRecurso(DescPedidoNovoRecurso="Quero um elevador novo",DataPedido=date.today(),UtilizadorID=1,EstadoPedNovoRecID=1))
    orcamento = OrcamentoSchema(IDEntidade=entidade.EntidadeID, Valor=100,DescOrcamento="Teste",NomePDF="Teste",IDProcesso=pedido_aquisicao.PedidoNovoRecID, TipoProcesso=TipoOrcamento.AQUISICAO)
    fake_pdf = AsyncMock(spec=UploadFile)
    fake_pdf.filename = "teste1.pdf"
    fake_pdf.file = BytesIO(b"conteudo de teste")
    fake_pdf.content_type = "application/pdf"
    result = await inserir_orcamento_service(db_session, orcamento, fake_pdf)
    id_orcamento = await get_last_id(db_session)
    orcamento_update = OrcamentoUpdateSchema(IDEntidade=entidade.EntidadeID,Valor=200,DescOrcamento="Teste mudado",OrcamentoID=id_orcamento.OrcamentoID)

    #Act
    result = await alterar_orcamento_service(db_session, orcamento_update,fake_pdf)

    #Assert
    assert result[0] == True
    assert result[1] == {'message': 'Inserção feita com sucesso'}
