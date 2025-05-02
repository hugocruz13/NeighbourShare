import unittest
import pytest
from unittest.mock import patch, MagicMock, Mock, mock_open, AsyncMock
from db.models import RecursoComun, EstadoManutencao, EstadoPedidoManutencao
from io import BytesIO
import sys
from pydantic import ValidationError, EmailStr, parse_obj_as
from datetime import date

sys.modules["db.session"] = MagicMock()

from services.recurso_comum_service import *

#region Gestão dos Recursos Comuns

@pytest.mark.asyncio
@patch("db.session.create_engine", return_value=MagicMock())
@patch("db.session.SessionLocal", return_value=MagicMock())
@patch("db.repository.recurso_comum_repo.inserir_recurso_comum_db", return_value=RecursoComun(
    Nome='Teste', DescRecursoComum='TesteDesc', Path="none", RecComumID=1))
@patch("services.recurso_comum_service.guardar_imagem", return_value='cleanpath/teste/teste.jpg')
@patch("db.repository.recurso_comum_repo.update_imagem", return_value=True)
async def test_inserir_recurso_comum_service(mock_create_engine, mock_sessionlocal,mock_inserir_recurso_comum_db, mock_guardar_imagem, mock_update_imagem):
    #Arrange

    fake_file_content = b"Hello world"
    file = UploadFile(filename="test.jpg", file=BytesIO(fake_file_content))

    #Act
    result = await inserir_recurso_comum_service(mock_sessionlocal,RecursoComumSchemaCreate(Nome='Teste', DescRecursoComum='TesteDec'),file)

    #Assert
    assert result.id == 1
    assert result.nome == "Teste"
    assert result.desc == "TesteDesc"
    assert result.path == "cleanpath/teste/teste.jpg"

@pytest.mark.asyncio
async def test_guardar_imagem():
    mock_file = Mock()
    mock_file.read.return_value = b"fake image content"

    imagem = Mock(spec=UploadFile)
    imagem.filename = "teste.jpg"
    imagem.content_type = "image/jpeg"
    imagem.file = mock_file

    with patch("os.getenv") as mock_getenv, \
            patch("os.makedirs") as mock_makedirs, \
            patch("builtins.open", mock_open()) as mock_file_open:

        # Define os valores retornados pelo getenv
        mock_getenv.side_effect = lambda x: {
            "UPLOAD_DIR_RECURSOCOMUM": "/fake/upload",
            "SAVE_RECURSOCOMUM": "/fake/url"
        }[x]

        resultado = await guardar_imagem(imagem, 123)

        esperado = "/fake/url/123/teste.jpg"
        resultado_normalizado = os.path.normpath(resultado).replace("\\", "/")

        assert resultado_normalizado == esperado

        mock_makedirs.assert_called_once_with("/fake/upload/123", exist_ok=True)
        mock_file_open.assert_called_once_with("/fake/upload/123/teste.jpg", 'wb+')
        mock_file.read.assert_called_once()

@pytest.mark.asyncio
@patch("services.recurso_comum_service.os.path.isfile")
@patch("services.recurso_comum_service.os.remove")
@patch("services.recurso_comum_service.os.listdir")
@patch("services.recurso_comum_service.os.getenv")
@patch("services.recurso_comum_service.guardar_imagem")
async def test_substitui_imagem_recurso_comum_service(mock_guardar_imagem, mock_getenv, mock_listdir, mock_remove, mock_isfile):
    # Definindo os mocks
    mock_getenv.side_effect = lambda var: {
        "UPLOAD_DIR_RECURSOCOMUM": "/fake/upload"
    }[var]

    mock_isfile.return_value = True

    # Criando o mock para a imagem
    mock_imagem = Mock(spec=UploadFile)
    mock_imagem.filename = "nova_imagem.jpg"
    mock_imagem.content_type = "image/jpeg"
    mock_imagem.file = BytesIO(b"fake image content")

    # Caso 1: Imagem é None, a função deve retornar False
    resultado = await substitui_imagem_recurso_comum_service(123, None)
    assert resultado == False

    # Caso 2: Tipo de imagem não permitido (a função deve lançar HTTPException)
    mock_imagem.content_type = "image/gif"
    with pytest.raises(HTTPException):
        await substitui_imagem_recurso_comum_service(123, mock_imagem)

    # Caso 3: A imagem já existe, a função deve retornar False
    mock_imagem.content_type = "image/jpg"
    mock_listdir.return_value = ["nova_imagem.jpg"]
    resultado = await substitui_imagem_recurso_comum_service(123, mock_imagem)
    assert resultado == False
    mock_remove.assert_not_called()  # A função não deve chamar os.remove, já que a imagem não será substituída
    mock_guardar_imagem.assert_not_called()

    # Caso 4: A imagem não existe, a função deve chamar guardar_imagem
    mock_listdir.return_value = ["outra_imagem.jpg"]
    mock_guardar_imagem.return_value = "/fake/upload/123/nova_imagem.jpg"

    resultado = await substitui_imagem_recurso_comum_service(123, mock_imagem)

    assert resultado == "/fake/upload/123/nova_imagem.jpg"
    mock_guardar_imagem.assert_called_once_with(mock_imagem, 123)

    # Verificando se os arquivos foram removidos
    mock_remove.assert_called_once_with("/fake/upload/123/outra_imagem.jpg")

@pytest.mark.asyncio
@pytest.mark.parametrize("mock_return, side_effect, recurso_id, expected_result, expect_exception", [
    # Caso de sucesso
    (MagicMock(), None, 1, "success", False),
    # Caso recurso não encontrado
    (None, HTTPException(status_code=404, detail="Recurso Comum não encontrado"), 99, "not_found", True),
    # Caso erro SQLAlchemy retornando dict de erro
    ({"details": "erro no banco"}, None, 2, {"details": "erro no banco"}, False),
])
async def test_update_recurso_comum(mock_return, side_effect, recurso_id, expected_result, expect_exception):
    # Arrange
    mock_db = MagicMock()
    recurso_update = RecursoComunUpdate(Nome="Nome atualizado")

    # Mock do repositório
    mock_repo = AsyncMock()
    if side_effect:
        mock_repo.side_effect = side_effect
    else:
        mock_repo.return_value = mock_return

    recurso_comum_repo.update_recurso_comum_db = mock_repo

    # Act & Assert
    if expect_exception:
        with pytest.raises(HTTPException) as exc_info:
            await update_recurso_comum_service(recurso_id, recurso_update, mock_db)
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Recurso Comum não encontrado"
    else:
        resultado = await update_recurso_comum_service(recurso_id, recurso_update, mock_db)
        if expected_result == "success":
            assert resultado == mock_return
        else:
            assert resultado == expected_result

    mock_repo.assert_awaited_once_with(recurso_id, recurso_update, mock_db)

@pytest.mark.asyncio
@pytest.mark.parametrize("pode_eliminar, resultado_esperado, expect_exception", [
    (True, {'Recurso Eliminado com sucesso!'}, False),  # Caso sucesso
    (False, {'Recurso comum numa pedido de manutenção ativo'}, False),  # Caso bloqueado
    (Exception("Erro inesperado"), None, True),  # Erro inesperado
])
@patch("services.recurso_comum_service.recurso_comum_repo.eliminar_recurso_comum_db")
@patch("services.recurso_comum_service.verificar_possibilidade_eliminar_recurso_comum_service")
async def test_eliminar_recurso_comum_service(mock_verifica, mock_eliminar, pode_eliminar, resultado_esperado, expect_exception):
    # Arrange
    recurso_id = 1
    mock_db = MagicMock()

    # Mocka o verificar_possibilidade_eliminar_recurso_comum_service
    if isinstance(pode_eliminar, Exception):
        mock_verifica.side_effect = pode_eliminar
    else:
        mock_verifica.return_value = pode_eliminar

    mock_eliminar.return_value = {'Recurso Eliminado com sucesso!'}

    # Act & Assert
    if expect_exception:
        with pytest.raises(Exception) as exc_info:
            await eliminar_recurso_comum_service(recurso_id, mock_db)
        assert "Erro inesperado" in str(exc_info.value)
    else:
        resultado = await eliminar_recurso_comum_service(recurso_id, mock_db)
        assert resultado == resultado_esperado

    # Verificações
    mock_verifica.assert_awaited_once_with(recurso_id, mock_db)

    if not expect_exception and pode_eliminar is True:
        mock_eliminar.assert_awaited_once_with(recurso_id, mock_db)
    else:
        mock_eliminar.assert_not_called()

@pytest.mark.asyncio
@pytest.mark.parametrize("repo_resultado, esperado, deve_lancar", [
    (True, True, False),
    (False, False, False),
    (Exception("Erro no banco"), None, True)
])
@patch("services.recurso_comum_service.recurso_comum_repo.verifica_eliminar_recurso_comum_db")
async def test_verificar_possibilidade_eliminar_recurso_comum_service(mock_repo, repo_resultado, esperado, deve_lancar):
    recurso_id = 1
    mock_db = MagicMock()

    # Define retorno ou exceção
    if isinstance(repo_resultado, Exception):
        mock_repo.side_effect = repo_resultado
    else:
        mock_repo.return_value = repo_resultado

    if deve_lancar:
        with pytest.raises(Exception) as exc_info:
            await verificar_possibilidade_eliminar_recurso_comum_service(recurso_id, mock_db)
        assert "Erro no banco" in str(exc_info.value)
    else:
        resultado = await verificar_possibilidade_eliminar_recurso_comum_service(recurso_id, mock_db)
        assert resultado == esperado

    mock_repo.assert_awaited_once_with(recurso_id, mock_db)

#endregion

#region Pedidos de Novos Recursos

@pytest.mark.asyncio
@patch("services.recurso_comum_service.notificacao_service.cria_notificacao_insercao_pedido_novo_recurso_comum_service")
@patch("services.recurso_comum_service.recurso_comum_repo.inserir_pedido_novo_recurso_db")
async def test_inserir_pedido_novo_recurso_service(mock_inserir_pedido_db, mock_criar_notificacao):
    # Arrange
    db = MagicMock()
    pedido_input = PedidoNovoRecursoSchemaCreate(
        UtilizadorID=1,
        DescPedidoNovoRecurso="Compra de projetor novo",
        DataPedido=date.today(),
        EstadoPedNovoRecID=1
    )

    # -------------------------------
    # CASO DE SUCESSO
    # -------------------------------
    mock_pedido_obj = MagicMock()
    mock_inserir_pedido_db.return_value = ({"Pedido de novo recurso inserido com sucesso!"}, mock_pedido_obj)
    mock_criar_notificacao.return_value = {"notificacao criada com sucesso"}

    # Act
    resultado_msg, resultado_noti = await inserir_pedido_novo_recurso_service(db, pedido_input)

    # Assert
    assert resultado_msg == {"Pedido de novo recurso inserido com sucesso!"}
    assert resultado_noti == {"notificacao criada com sucesso"}
    mock_inserir_pedido_db.assert_awaited_once_with(db, pedido_input)
    mock_criar_notificacao.assert_awaited_once_with(db, mock_pedido_obj)

    # -------------------------------
    # CASO DE ERRO
    # -------------------------------
    mock_inserir_pedido_db.reset_mock()
    mock_criar_notificacao.reset_mock()

    mock_inserir_pedido_db.side_effect = Exception("Erro no banco")

    with pytest.raises(HTTPException) as exc_info:
        await inserir_pedido_novo_recurso_service(db, pedido_input)

    assert exc_info.value.status_code == 500
    assert "Erro no banco" in str(exc_info.value.detail)
    mock_inserir_pedido_db.assert_awaited_once_with(db, pedido_input)
    mock_criar_notificacao.assert_not_called()

#endregion

#region Pedidos de Manutenção

@pytest.mark.asyncio
@patch("services.recurso_comum_service.notificacao_service.cria_notificacao_insercao_pedido_manutencao_service")
@patch("services.recurso_comum_service.recurso_comum_repo.inserir_pedido_manutencao_db")
async def test_inserir_pedido_manutencao_service(mock_inserir_pedido_db, mock_criar_notificacao):
    # Arrange
    db = MagicMock()
    pedido_input = PedidoManutencaoSchemaCreate(
        UtilizadorID=1,
        RecComumID=1,
        DescPedido="Manutenção do ar-condicionado",
        DataPedido=date.today(),
        EstadoPedManuID=1
    )

    # -------------------------------
    # CASO DE SUCESSO
    # -------------------------------
    mock_pedido_obj = MagicMock()
    mock_inserir_pedido_db.return_value = ({"Pedido de manutenção inserido com sucesso!"}, mock_pedido_obj)
    mock_criar_notificacao.return_value = {"notificação criada com sucesso"}

    # Act
    resultado_msg, resultado_noti = await inserir_pedido_manutencao_service(db, pedido_input)

    # Assert
    assert resultado_msg == {"Pedido de manutenção inserido com sucesso!"}
    assert resultado_noti == {"notificação criada com sucesso"}
    mock_inserir_pedido_db.assert_awaited_once_with(db, pedido_input)
    mock_criar_notificacao.assert_awaited_once_with(db, mock_pedido_obj)

    # -------------------------------
    # CASO DE ERRO
    # -------------------------------
    mock_inserir_pedido_db.reset_mock()
    mock_criar_notificacao.reset_mock()

    mock_inserir_pedido_db.side_effect = Exception("Erro ao inserir no banco")

    with pytest.raises(HTTPException) as exc_info:
        await inserir_pedido_manutencao_service(db, pedido_input)

    assert exc_info.value.status_code == 500
    assert "Erro ao inserir no banco" in str(exc_info.value.detail)
    mock_inserir_pedido_db.assert_awaited_once_with(db, pedido_input)
    mock_criar_notificacao.assert_not_called()


@pytest.mark.asyncio
@patch("services.recurso_comum_service.recurso_comum_repo.obter_all_tipo_estado_pedido_manutencao")
@patch("services.recurso_comum_service.recurso_comum_repo.alterar_estado_pedido_manutencao")
@patch("services.recurso_comum_service.notificacao_service.cria_notificacao_nao_necessidade_entidade_externa")
@patch("services.recurso_comum_service.notificacao_service.cria_notificacao_necessidade_entidade_externa")
@patch("services.recurso_comum_service.notificacao_service.cria_notificacao_rejeicao_manutencao_recurso_comum")
@patch("services.recurso_comum_service.recurso_comum_repo.obter_pedido_manutencao_db")
async def test_alterar_tipo_estado_pedido_manutencao(mock_obter_pedido_manutencao,
                                                     mock_criar_notificacao_rejeicao,
                                                     mock_criar_notificacao_necessidade,
                                                     mock_criar_notificacao_nao_necessidade,
                                                     mock_alterar_estado_pedido_manutencao,
                                                     mock_obter_all_estados):
    db = MagicMock()
    id_pedido_manutencao = 1
    tipo_estado_pedido_manutencao = 3

    # Dados de simulação
    mock_obter_all_estados.return_value = [
        EstadoPedidoManutencao(EstadoPedManuID=1, DescEstadoPedidoManutencao="Em Andamento"),
        EstadoPedidoManutencao(EstadoPedManuID=2, DescEstadoPedidoManutencao="Aprovado para manutenção interna"),
        EstadoPedidoManutencao(EstadoPedManuID=3, DescEstadoPedidoManutencao="Em negociação com entidades externas"),
        EstadoPedidoManutencao(EstadoPedManuID=4, DescEstadoPedidoManutencao="Rejeitado")
    ]

    # Mock para obter o pedido de manutenção
    mock_obter_pedido_manutencao.return_value = PedidoManutencaoSchema(
        PMID=1,
        Utilizador_=MagicMock(NomeUtilizador="José", UtilizadorID=1),
        RecursoComun_=MagicMock(RecComumID=1, Nome="Elevador", DescRecursoComum= "TestedeDesc"),
        DescPedido="Reparo no elevador",
        DataPedido=datetime.date.today(),
        EstadoPedidoManutencao_=MagicMock(EstadoPedManuID=3, DescEstadoPedidoManutencao="Aprovado para manutenção interna")
    )

    # -------------------------------
    # CASO DE SUCESSO
    # -------------------------------
    # Simula sucesso na alteração do estado e notificação para a necessidade de entidade externa
    mock_alterar_estado_pedido_manutencao.return_value = True
    mock_criar_notificacao_nao_necessidade.return_value = True

    resultado = await alterar_tipo_estado_pedido_manutencao(db, id_pedido_manutencao, tipo_estado_pedido_manutencao)

    assert resultado is True
    mock_alterar_estado_pedido_manutencao.assert_called_once_with(db, id_pedido_manutencao,
                                                                  tipo_estado_pedido_manutencao)
    mock_criar_notificacao_necessidade.assert_called_once()

    # -------------------------------
    # CASO DE ERRO - Tipo de estado não encontrado
    # -------------------------------
    tipo_estado_pedido_manutencao_invalido = 5  # Estado inválido
    resultado_invalido = await alterar_tipo_estado_pedido_manutencao(db, id_pedido_manutencao,
                                                                     tipo_estado_pedido_manutencao_invalido)

    assert resultado_invalido is False


@pytest.mark.asyncio
@patch("services.recurso_comum_service.recurso_comum_repo.obter_pedido_manutencao_db")
@patch("services.recurso_comum_service.recurso_comum_repo.update_pedido_manutencao_db")
async def test_update_pedido_manutencao(mock_update_pedido, mock_obter_pedido):
    # Arrange
    db = MagicMock()

    # Simulação de um pedido de manutenção já existente
    pedido_manutencao = MagicMock()
    pedido_manutencao.PMID = 1
    pedido_manutencao.DescPedido = "Reparo no elevador"
    pedido_manutencao.DataPedido = datetime.date.today()
    pedido_manutencao.RecComumID = 1
    pedido_manutencao.EstadoPedManuID = 1
    pedido_manutencao.VotacaoID = None
    pedido_manutencao.UtilizadorID = 1  # O "ID" do utilizador que criou o pedido

    # Mock para o comportamento de obter o pedido de manutenção
    mock_obter_pedido.return_value = pedido_manutencao

    # Simulação do "token" de um utilizador
    token_residente = UserJWT(id=1, email=parse_obj_as(EmailStr, "exemplo@dominio.com"),
                              role="residente")  # Este utilizador é o proprietário do pedido
    token_admin = UserJWT(id=2, email=parse_obj_as(EmailStr, "exemplo@dominio.com"), role="admin")  # Um utilizador administrador

    # Dados para atualização do pedido
    u_pedido = PedidoManutencaoUpdateSchema(PMID=1, DescPedido="Reparo no elevador - Atualizado")

    # -------------------------------
    # CASO DE SUCESSO
    # -------------------------------
    mock_update_pedido.return_value = pedido_manutencao

    # Act
    sucesso, mensagem = await update_pedido_manutencao(db, u_pedido, token_residente)

    # Assert
    assert sucesso is True
    assert mensagem == pedido_manutencao

    # -------------------------------
    # CASO DE ERRO: Descrição não fornecida
    # -------------------------------

    # Verifica se a exceção de validação ocorre ao tentar validar o modelo
    with pytest.raises(ValidationError):
        u_pedido_invalido = PedidoManutencaoUpdateSchema(PMID=1, DescPedido=str(None))

    # -------------------------------
    # CASO DE ERRO: Utilizador sem permissão
    # -------------------------------
    u_pedido_validado = PedidoManutencaoUpdateSchema(PMID=1, DescPedido='Test123454')

    # O "token" é de um administrador, mas o pedido pertence a um residente com "ID" 1
    sucesso, mensagem = await update_pedido_manutencao(db, u_pedido_validado, token_admin)

    # Assert
    assert sucesso is False
    assert mensagem == "Utilizador não têm permissão para alterar os dados do pedido de manutenção"


# Teste completo para eliminar pedido de manutenção
@pytest.mark.asyncio
@patch("services.recurso_comum_service.recurso_comum_repo.eliminar_pedido_manutencao")
@patch("services.recurso_comum_service.obter_pedido_manutencao")
async def test_eliminar_pedido_manutencao(mock_obter_pedido_manutencao, mock_eliminar_pedido_manutencao):
    # Mock para o db (base de dados)
    db = MagicMock(Session)

    # Mock para o token_residente
    token_residente = MagicMock()
    token_residente.id = 1  # Utilizador com "ID" 1
    token_residente.role = "residente"  # Utilizador é residente

    # Mock de exemplo de pedido de manutenção
    pedido_id = 1

    # Mock do pedido de manutenção que será retornado
    pedido_manutencao_mock = MagicMock()
    pedido_manutencao_mock.UtilizadorID = 1  # O pedido pertence ao residente
    mock_obter_pedido_manutencao.return_value = pedido_manutencao_mock  # Retorna o pedido de manutenção mockado

    # Mock da função eliminar_pedido_manutencao para simular a eliminação do pedido
    mock_eliminar_pedido_manutencao.return_value = {'Pedido de manutenção eliminado com sucesso!'}

    # -------------------------------
    # CASO DE SUCESSO
    # -------------------------------
    resposta = await eliminar_pedido_manutencao_service(db, pedido_id, token_residente)

    # Verificando a resposta
    assert resposta == {'Pedido de manutenção eliminado com sucesso!'}

    # -------------------------------
    # CASO DE ERRO - PERMISSÃO NEGADA
    # -------------------------------
    # Simula um residente tentando excluir o pedido de manutenção de outro residente
    token_residente.id = 2  # Simulando outro residente que não tem permissão para excluir o pedido

    resposta = await eliminar_pedido_manutencao_service(db, pedido_id, token_residente)

    # Verificando a mensagem de erro de permissão negada
    assert resposta == {'Utilizador não têm permissão para alterar os dados do pedido de manutenção'}

    # -------------------------------
    # CASO DE ERRO - EXCEÇÃO NA ELIMINAÇÃO (PEDIDO NÃO ENCONTRADO)
    # -------------------------------
    # Mock para simular que o pedido de manutenção não existe
    mock_obter_pedido_manutencao.return_value = None

    # Verificando se uma exceção será lançada
    with pytest.raises(HTTPException):
        await eliminar_pedido_manutencao_service(db, pedido_id, token_residente)

#endregion

#region Manutenções

# Teste para o serviço de criação de manutenção
@pytest.mark.asyncio
@patch("services.recurso_comum_service.recurso_comum_repo.obter_pedido_manutencao_db")
@patch("db.repository.orcamento_repo.get_orcamento_by_id")
@patch("services.recurso_comum_service.recurso_comum_repo.criar_manutencao_db")
async def test_criar_manutencao_service(mock_criar_manutencao_db, mock_get_orcamento_by_id,
                                        mock_obter_pedido_manutencao_db):
    # Mock para o db
    db = MagicMock()

    # Mock de exemplo para o schema ManutencaoCreateSchema
    manutencao_data = ManutencaoCreateSchema(
        PMID=1,
        DataManutencao=date(2025, 5, 2),
        DescManutencao="Reparo no elevador",
        Orcamento_id=1
    )

    # Mock do pedido de manutenção
    pedido_manutencao_mock = MagicMock()
    pedido_manutencao_mock.PMID = 1
    mock_obter_pedido_manutencao_db.return_value = pedido_manutencao_mock

    # Mock do orçamento
    orcamento_mock = MagicMock()
    orcamento_mock.OrcamentoID = 1
    mock_get_orcamento_by_id.return_value = orcamento_mock

    # -------------------------------
    # CASO DE SUCESSO: Pedido e Orçamento existem
    # -------------------------------
    mock_criar_manutencao_db.return_value = {'Nova manutenção adicionada com sucesso !'}

    sucesso = await criar_manutencao_service(db, manutencao_data)

    # Verificando a resposta
    assert sucesso == {'Nova manutenção adicionada com sucesso !'}

    # -------------------------------
    # CASO DE ERRO: Pedido de manutenção não encontrado
    # -------------------------------
    mock_obter_pedido_manutencao_db.return_value = None  # Simulando pedido não encontrado

    with pytest.raises(HTTPException):
        await criar_manutencao_service(db, manutencao_data)

@pytest.mark.asyncio
@patch("services.recurso_comum_service.recurso_comum_repo.obter_all_tipo_estado_manutencao")
@patch("services.recurso_comum_service.recurso_comum_repo.alterar_estado_manutencao")
async def test_alterar_tipo_estado_manutencao(mock_alterar_estado_manutencao,mock_obter_all_estados):
    # Arrange
    db = MagicMock()
    id_manutencao = 1
    tipo_estado_manutencao = 2  # Exemplo: 2 representa o estado "Concluída"

    # -------------------------------
    # CASO DE SUCESSO
    # -------------------------------
    # Mocka uma lista de objetos EstadoManutencao
    mock_obter_all_estados.return_value = [
        EstadoManutencao(EstadoManuID=1, DescEstadoManutencao="Em Andamento"),
        EstadoManutencao(EstadoManuID=2, DescEstadoManutencao="Concluída"),
        EstadoManutencao(EstadoManuID=3, DescEstadoManutencao="Cancelada")
    ]

    # Simula que a alteração foi realizada com sucesso
    mock_alterar_estado_manutencao.return_value = True

    # Act
    resultado = await alterar_tipo_estado_manutencao(db, id_manutencao, tipo_estado_manutencao)

    # Assert
    assert resultado is True
    mock_obter_all_estados.assert_awaited_once_with(db)
    mock_alterar_estado_manutencao.assert_awaited_once_with(db, id_manutencao, tipo_estado_manutencao)

    # -------------------------------
    # CASO DE ERRO - Tipos de estado não obtidos
    # -------------------------------
    mock_obter_all_estados.reset_mock()
    mock_alterar_estado_manutencao.reset_mock()

    mock_obter_all_estados.return_value = None  # Simula que não foi possível obter os estados

    with pytest.raises(HTTPException) as exc_info:
        await alterar_tipo_estado_manutencao(db, id_manutencao, tipo_estado_manutencao)

    assert exc_info.value.status_code == 500
    assert "Erro ao obter tipos de estado manutenção" in str(exc_info.value.detail)
    mock_obter_all_estados.assert_awaited_once_with(db)
    mock_alterar_estado_manutencao.assert_not_called()

    # -------------------------------
    # CASO DE ERRO - Tipo de estado inválido
    # -------------------------------
    mock_obter_all_estados.reset_mock()
    mock_alterar_estado_manutencao.reset_mock()

    mock_obter_all_estados.return_value = [
        EstadoManutencao(EstadoManuID=1, DescEstadoManutencao="Em Andamento"),
        EstadoManutencao(EstadoManuID=2, DescEstadoManutencao="Concluída"),
        EstadoManutencao(EstadoManuID=3, DescEstadoManutencao="Cancelada")
    ]  # Tipos de estado válidos

    # Tipo de estado inválido
    tipo_estado_manutencao_invalido = 4  # Um tipo que não existe na lista

    resultado = await alterar_tipo_estado_manutencao(db, id_manutencao,tipo_estado_manutencao_invalido)

    # Assert
    assert resultado is False
    mock_obter_all_estados.assert_awaited_once_with(db)
    mock_alterar_estado_manutencao.assert_not_called()


@pytest.mark.asyncio
@patch("services.recurso_comum_service.recurso_comum_repo.obter_manutencao_db")
async def test_obter_manutencao_service(mock_obter_manutencao_db):
    # Mock para o db
    db = MagicMock()

    # Mock de exemplo para a manutenção
    manutencao_mock = MagicMock()
    manutencao_mock.PMID = 1
    manutencao_mock.DescManutencao = "Reparo no elevador"
    mock_obter_manutencao_db.return_value = manutencao_mock

    # -------------------------------
    # CASO DE SUCESSO: Manutenção encontrada
    # -------------------------------
    manutencao = await obter_manutencao(db, 1)

    # Verificando a resposta
    assert manutencao.PMID == 1
    assert manutencao.DescManutencao == "Reparo no elevador"

    # -------------------------------
    # CASO DE ERRO: Manutenção não encontrada (Simulando falha no DB)
    # -------------------------------
    mock_obter_manutencao_db.return_value = None  # Simulando que não encontrou manutenção

    with pytest.raises(HTTPException):
        await obter_manutencao(db, 1)

    # -------------------------------
    # CASO DE ERRO: Erro no banco de dados (Simulando exceção)
    # -------------------------------
    mock_obter_manutencao_db.side_effect = SQLAlchemyError("Database error")  # Simulando erro no DB

    with pytest.raises(HTTPException):
        await obter_manutencao(db, 1)

@pytest.mark.asyncio
@patch("services.recurso_comum_service.recurso_comum_repo.update_manutencao_db")
async def test_update_manutencao_service(mock_update_manutencao_db):
    # Mock do db
    db = MagicMock()

    # Dados válidos
    manutencao_data = ManutencaoUpdateSchema(
        ManutencaoID=1,
        PMID=2,
        DataManutencao=date(2025, 5, 2),
        DescManutencao="Atualização da pintura"
    )

    # -------------------------------
    # CASO DE SUCESSO
    # -------------------------------
    manutencao_mock = MagicMock()
    manutencao_mock.ManutencaoID = 1
    mock_update_manutencao_db.return_value = manutencao_mock

    resultado = await update_manutencao(db, manutencao_data)
    assert resultado.ManutencaoID == 1
    mock_update_manutencao_db.assert_called_once()

    # -------------------------------
    # CASO DE ERRO: Repositório retorna None
    # -------------------------------
    mock_update_manutencao_db.reset_mock()
    mock_update_manutencao_db.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await update_manutencao(db, manutencao_data)
    assert exc_info.value.status_code == 500
    assert "Erro, a atualizar manutenção" in exc_info.value.detail

    # -------------------------------
    # CASO DE ERRO: SQLAlchemyError
    # -------------------------------
    mock_update_manutencao_db.side_effect = SQLAlchemyError("Erro no banco")

    with pytest.raises(HTTPException) as exc_info:
        await update_manutencao(db, manutencao_data)
    assert exc_info.value.status_code == 500
    assert "Erro no banco" in exc_info.value.detail

@pytest.mark.asyncio
@patch("services.recurso_comum_service.recurso_comum_repo.eliminar_manutencao_db")
async def test_eliminar_manutencao_service(mock_eliminar_manutencao_db):
    # Mock do DB
    db = MagicMock()

    # -------------------------------
    # CASO DE SUCESSO
    # -------------------------------
    mock_eliminar_manutencao_db.return_value = {'Manutenção eliminada com sucesso!'}

    resposta = await eliminar_manutencao_service(db, 1)
    assert resposta == {'Manutenção eliminada com sucesso!'}
    mock_eliminar_manutencao_db.assert_called_once_with(db, 1)

    # -------------------------------
    # CASO DE ERRO: Exceção SQLAlchemy
    # -------------------------------
    mock_eliminar_manutencao_db.side_effect = SQLAlchemyError("Erro ao eliminar")

    with pytest.raises(HTTPException) as exc_info:
        await eliminar_manutencao_service(db, 1)

    assert exc_info.value.status_code == 500
    assert "Erro ao eliminar" in exc_info.value.detail

#endregion


if __name__ == '__main__':
    unittest.main()
