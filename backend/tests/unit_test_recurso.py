from unittest.mock import patch, MagicMock, AsyncMock
import pytest
from fastapi import HTTPException
from schemas.recurso_schema import RecursoInserirSchema
from services import recurso_service
from services.recurso_service import lista_recursos_service, lista_recurso_service


@pytest.fixture
def db_session():
    from db.session import get_db
    return next(get_db())

async def test_get_disponibilidade_id_service_success(db_session):
    result = await recurso_service.get_disponibilidade_id_service(db_session, "Disponível")
    assert result == 1

async def test_get_disponibilidade_id_service_failure():
    # Simula uma exceção genérica no repo (não HTTPException)
    mock_db = MagicMock()
    with patch("services.recurso_service.recurso_repo.get_disponibilidade_id_db", side_effect=Exception("Erro inesperado")):
        with pytest.raises(HTTPException) as exc_info:
            await recurso_service.get_disponibilidade_id_service(mock_db, "Indisponível")
        assert exc_info.value.status_code == 500
        assert "Erro inesperado" in exc_info.value.detail

async def test_get_categoria_id_service_success(db_session):
    result = await recurso_service.get_categoria_id_service(db_session, "Lazer")
    assert result == 1

async def test_get_categoria_id_service_failure():
    mock_db = MagicMock()
    with patch("services.recurso_service.recurso_repo.get_categoria_id_db", side_effect=Exception("Erro inesperado")):
        with pytest.raises(HTTPException) as exc_info:
            await recurso_service.get_categoria_id_service(mock_db, "CategoriaDesconhecida")
        assert exc_info.value.status_code == 500
        assert "Erro inesperado" in exc_info.value.detail

async def test_inserir_recurso_service_success(db_session):
    novo_recurso = RecursoInserirSchema(
        Nome="RecursoTeste",
        DescRecurso="Recurso para teste uni",
        UtilizadorID=1,
        Caucao=50,
        CatID=1,
        DispID=1,
    )
    class DummyUpload:
        content_type = 'image/jpeg'
        filename = "testeimg.jpg"
        file = open(__file__, "rb")
    imagem = DummyUpload()
    from os import environ
    environ["UPLOAD_DIR_PERFIL"] = "."
    environ["SAVE_PERFIL"] = "."

    result = await recurso_service.inserir_recurso_service(db_session, novo_recurso, imagem)
    assert result == (True, {"message": "Imagem guardada com sucesso"})

async def test_inserir_recurso_service_failure(db_session):
    # Simula um erro genérico durante a inserção
        with pytest.raises(HTTPException) as exc_info:
            await recurso_service.inserir_recurso_service(db_session, None, None)
        assert exc_info.value.status_code == 500

async def test_guardar_imagem_recurso_tipo_invalido():
    imagem_recurso = MagicMock()
    imagem_recurso.content_type = 'application/pdf'  # tipo não permitido
    mock_db = MagicMock()
    with pytest.raises(HTTPException) as exc_info:
        await recurso_service.guardar_imagem_recurso(imagem_recurso, 1, mock_db)
    assert exc_info.value.status_code == 400
    assert "Apenas imagens são permitidas" in exc_info.value.detail

async def test_guardar_imagem_recurso_sucesso(tmp_path):
    imagem_recurso = MagicMock()
    imagem_recurso.content_type = 'image/png'
    imagem_recurso.filename = 'teste.png'
    imagem_recurso.file.read.return_value = b'test_content'
    recurso_id = 10
    mock_db = MagicMock()

    # Substituindo variáveis de ambiente e métodos externos
    with patch("services.recurso_service.os.getenv") as mock_getenv, \
         patch("services.recurso_service.open", create=True) as mock_open, \
         patch("services.recurso_service.recurso_repo.update_path", new=AsyncMock(return_value=True)):
        mock_getenv.side_effect = lambda name: str(tmp_path)  # Força ambos caminhos para tmp_path

        file_mock = MagicMock()
        mock_open.return_value.__enter__.return_value = file_mock

        result = await recurso_service.guardar_imagem_recurso(imagem_recurso, recurso_id, mock_db)
        assert result == (True, {"message": "Imagem guardada com sucesso"})
        file_mock.write.assert_called_once_with(b'test_content')

async def test_guardar_imagem_recurso_falha_update(tmp_path):
    imagem_recurso = MagicMock()
    imagem_recurso.content_type = 'image/jpeg'
    imagem_recurso.filename = 'teste.jpg'
    imagem_recurso.file.read.return_value = b'teste'
    recurso_id = 20
    mock_db = MagicMock()

    with patch("services.recurso_service.os.getenv") as mock_getenv, \
         patch("services.recurso_service.open", create=True) as mock_open, \
         patch("services.recurso_service.recurso_repo.update_path", new=AsyncMock(return_value=False)):
        mock_getenv.side_effect = lambda name: str(tmp_path)
        file_mock = MagicMock()
        mock_open.return_value.__enter__.return_value = file_mock

        result = await recurso_service.guardar_imagem_recurso(imagem_recurso, recurso_id, mock_db)
        assert result == (False, {"message": "Erro ao guardada imagem"})

async def test_guardar_imagem_recurso_exception_interna(tmp_path):
    imagem_recurso = MagicMock()
    imagem_recurso.content_type = 'image/png'
    imagem_recurso.filename = 'bad.png'
    imagem_recurso.file.read.side_effect = Exception("Falha ao ler arquivo")
    recurso_id = 99
    mock_db = MagicMock()

    with patch("services.recurso_service.os.getenv", return_value=str(tmp_path)), \
         patch("services.recurso_service.os.makedirs"), \
         patch("services.recurso_service.open", create=True):
        with pytest.raises(HTTPException) as exc_info:
            await recurso_service.guardar_imagem_recurso(imagem_recurso, recurso_id, mock_db)
        assert exc_info.value.status_code == 500
        assert "Falha ao ler arquivo" in exc_info.value.detail

async def test_lista_recursos_service_sucesso(db_session):
    # Certifique-se de que há pelo menos um recurso válido existente no banco!
    resultado = await lista_recursos_service(db_session)
    assert resultado is not None
    assert isinstance(resultado, list)
    assert len(resultado) > 0
    # Verifica se pelo menos um recurso tem os campos esperados
    recurso = resultado[0]
    assert hasattr(recurso, "Nome")
    assert hasattr(recurso, "Image")

@patch('services.recurso_service.lista_imagens_recursos_service')
@patch('services.recurso_service.recurso_repo')
async def test_lista_recursos_service_sem_recursos(mock_recurso_repo, mock_lista_imagens):
    mock_db = MagicMock()
    mock_recurso_repo.listar_recursos_db = AsyncMock(return_value=[])
    with pytest.raises(HTTPException) as exc:
        await lista_recursos_service(mock_db)
    assert exc.value.status_code == 400
    assert "Nenhum recurso encontrado" in str(exc.value.detail)
    mock_lista_imagens.assert_not_called()

@patch('services.recurso_service.lista_imagens_recursos_service')
@patch('services.recurso_service.recurso_repo')
async def test_lista_recursos_service_erro_na_imagem(mock_recurso_repo, mock_lista_imagens):
    mock_db = MagicMock()
    recursos = [MagicMock()]
    mock_recurso_repo.listar_recursos_db = AsyncMock(return_value=recursos)
    mock_lista_imagens.return_value = None

    with pytest.raises(HTTPException) as exc:
        await lista_recursos_service(mock_db)
    assert exc.value.status_code == 400
    assert "Erro no carregameto das imagens dos recursos" in str(exc.value.detail)

async def test_lista_recurso_service_sucesso(db_session):
    # Supondo que existe um recurso com ID 1 no banco de testes
    recurso_id = 2
    recurso = await lista_recurso_service(db_session, recurso_id)
    assert recurso is not None
    assert hasattr(recurso, "Image")  # Verifica se atribuiu o campo Image
    assert recurso.Image == recurso.Path

async def test_lista_recurso_service_nao_encontrado(db_session):
    recurso_id = 9999  # Um ID que certamente não existe no banco de testes
    with pytest.raises(HTTPException) as exc:
        await lista_recurso_service(db_session, recurso_id)
    assert exc.value.status_code == 400
    assert "Nenhum recurso encontrado" in str(exc.value.detail)
