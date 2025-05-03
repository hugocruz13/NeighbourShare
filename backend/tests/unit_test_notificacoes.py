import unittest
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from schemas.votacao_schema import TipoVotacao
import sys

sys.modules["db.session"] = MagicMock()

from services.notificacao_service import *

@pytest.mark.asyncio
@patch("services.notificacao_service.marcar_notificacao_lida_db")
@pytest.mark.parametrize("should_raise_exception", [False, True])
async def test_marcar_noti_lida_service(mock_marcar_noti_db, should_raise_exception):
    # Arrange
    db = MagicMock()
    notificacao_id = 1

    if should_raise_exception:
        mock_marcar_noti_db.side_effect = Exception("Erro inesperado")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await marcar_noti_lida_service(db, notificacao_id)
        assert exc_info.value.status_code == 500
        assert str(exc_info.value.detail) == "Erro inesperado"
    else:
        expected_response = {'Notificação marcada como lida!'}
        mock_marcar_noti_db.return_value = expected_response

        # Act
        result = await marcar_noti_lida_service(db, notificacao_id)

        # Assert
        assert result == expected_response
        mock_marcar_noti_db.assert_awaited_once_with(db, notificacao_id)

@pytest.mark.asyncio
@patch("services.notificacao_service.cria_notificacao_todos_utilizadores_db")
@patch("services.notificacao_service.get_tipo_processo_id")
@pytest.mark.parametrize("service_func", [
    cria_notificacao_decisao_novo_recurso_comum_service,
    cria_notificao_decisao_orcamento_novo_recurso_service,
    cria_notificacao_decisao_orcamento_manutencao_service
])
@pytest.mark.parametrize("should_raise_exception", [False, True])
async def test_cria_notificacoes_votacoes_services(
    mock_get_tipo_proc_id,
    mock_cria_notif_db,
    service_func,
    should_raise_exception
):
    # Arrange
    db = MagicMock()

    tipo_votacao = TipoVotacao.AQUISICAO

    if service_func is cria_notificao_decisao_orcamento_novo_recurso_service:
        tipo_votacao = TipoVotacao.AQUISICAO
    elif service_func is cria_notificacao_decisao_orcamento_manutencao_service:
        tipo_votacao = TipoVotacao.MANUTENCAO
    elif service_func is cria_notificacao_decisao_novo_recurso_comum_service:
        tipo_votacao = TipoVotacao.AQUISICAO

    votacao = Criar_Votacao(
        titulo="Título Teste",
        descricao="Descrição da votação",
        id_processo=10,
        data_fim=datetime.date(2025, 12, 31),
        tipo_votacao=tipo_votacao
    )

    if should_raise_exception:
        mock_get_tipo_proc_id.side_effect = Exception("Erro inesperado")
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await service_func(db, votacao)
        assert exc_info.value.status_code == 500
        assert str(exc_info.value.detail) == "Erro inesperado"
    else:
        tipo_proc_id = 99
        expected_response = (True, {'Inserção de notifcações para todos os utilizadores realizada com sucesso!'})
        mock_get_tipo_proc_id.return_value = tipo_proc_id
        mock_cria_notif_db.return_value = expected_response

        # Act
        result = await service_func(db, votacao)

        # Assert
        assert result == expected_response
        mock_get_tipo_proc_id.assert_awaited_once_with(db, TipoProcessoOpcoes.VOTACAO)
        mock_cria_notif_db.assert_awaited_once()

@pytest.mark.asyncio
@pytest.mark.parametrize("service_func,expected_phrase", [
    (cria_notificacao_decisao_compra_recurso_positiva_service, "foi aprovada por maioria a aquisição"),
    (cria_notificacao_decisao_nao_compra_recurso_service, "foi recusada por maioria a aquisição"),
])
async def test_cria_notificacao_decisao_compra_ou_nao_service(service_func, expected_phrase):
    # Arrange
    db = MagicMock()

    votacao = Votacao(
        VotacaoID=1,
        Titulo="Teste Votação",
        Descricao="Descrição da votação",
        DataInicio=datetime.date.today(),
        DataFim=datetime.date.today(),
        Processada=True
    )

    pedido = PedidoNovoRecursoSchema(
        PedidoNovoRecID=123,
        Utilizador_=UtilizadorSchema(UtilizadorID=1, NomeUtilizador='Teste', Contacto=123456778),
        DescPedidoNovoRecurso="Comprar equipamento novo",
        DataPedido=datetime.date.today(),
        EstadoPedidoNovoRecurso_=EstadoPedNovoRecursoSchema(EstadoPedNovoRecID=1,DescEstadoPedidoNovoRecurso="Pendente",)
    )

    with patch("services.notificacao_service.get_tipo_processo_id", new=AsyncMock(return_value=99)) as mock_get_tipo_proc_id, \
         patch("services.notificacao_service.cria_notificacao_todos_utilizadores_db", new=AsyncMock(return_value=(True, "ok"))) as mock_cria_notif_db:

        # Act
        result = await service_func(db, votacao, pedido)

        # Assert retorno
        assert result == (True, "ok")

        # Verifica se mocks foram usados
        mock_get_tipo_proc_id.assert_awaited_once()
        mock_cria_notif_db.assert_awaited_once()

        # Verifica conteúdo da mensagem
        args, _ = mock_cria_notif_db.call_args
        notificacao_enviada = args[1]
        assert isinstance(notificacao_enviada.Mensagem, str)
        assert expected_phrase in notificacao_enviada.Mensagem
        assert votacao.Titulo in notificacao_enviada.Mensagem
        assert votacao.Descricao in notificacao_enviada.Mensagem


@pytest.mark.asyncio
@pytest.mark.parametrize("service_func,expected_title,expected_user_msg", [
    (cria_notificacao_insercao_pedido_manutencao_service, "Novo Pedido de Manutenção de Recurso Comum Submetido", None),
    (cria_notificacao_nao_necessidade_entidade_externa, "Atualização sobre o seu pedido de manutenção",
     "não será necessária a intervenção de uma entidade externa"),
    (cria_notificacao_necessidade_entidade_externa, "Atualização sobre o seu pedido de manutenção",
     "verificamos a necessidade da intervenção de uma entidade externa"),
    (cria_notificacao_rejeicao_manutencao_recurso_comum, "Atualização sobre o seu pedido de manutenção",
     "não foi verificado uma intervenção no recurso")
])
async def test_cria_notificacao_pedido_manutencao_service(service_func, expected_title, expected_user_msg):
    # Arrange
    db = MagicMock()

    # Mock do PedidoManutencaoSchema
    pedido = PedidoManutencaoSchema(
        PMID=123,
        Utilizador_=UtilizadorSchema(UtilizadorID=1, NomeUtilizador='Teste', Contacto=123456778),
        RecursoComun_=RecursoComunSchema(RecComumID=456, Nome="Piscina", DescRecursoComum="Piscina do condomínio"),
        DescPedido="Manutenção na piscina",
        DataPedido=datetime.date.today(),
        EstadoPedidoManutencao_=EstadoPedManuSchema(EstadoPedManuID=1, DescEstadoPedidoManutencao="Em avaliação")
    )

    with patch("services.notificacao_service.get_tipo_processo_id",
               new=AsyncMock(return_value=99)) as mock_get_tipo_proc_id, \
            patch("services.notificacao_service.cria_notificacao_todos_utilizadores_db",
                  new=AsyncMock(return_value=(True, "ok"))) as mock_cria_notif_db, \
            patch("services.notificacao_service.cria_notificacao_admin_db",
                  new=AsyncMock(return_value=(True, "ok"))) as mock_cria_notif_admin_db, \
            patch("services.notificacao_service.cria_notificacao_individual_db",
                  new=AsyncMock(return_value=(True, "ok"))) as mock_cria_notif_individual_db:

        # Act
        result = await service_func(db, pedido)

        # Debugging - Verificando se mocks estão sendo chamados
        print(f"Result: {result}")
        print(f"Mock criao_notificacao_todos_utilizadores_db called: {mock_cria_notif_db.await_count}")
        print(f"Mock criao_notificacao_admin_db called: {mock_cria_notif_admin_db.await_count}")
        print(f"Mock criao_notificacao_individual_db called: {mock_cria_notif_individual_db.await_count}")

        # Assert retorno
        assert result == (True, "ok")

        # Verifica se mocks foram chamados corretamente
        mock_get_tipo_proc_id.assert_awaited_once()

        # Condicional para verificar qual função de notificação foi chamada
        if service_func == cria_notificacao_insercao_pedido_manutencao_service:
            mock_cria_notif_admin_db.assert_awaited_once()
        elif service_func == cria_notificacao_necessidade_entidade_externa:
            mock_cria_notif_db.assert_awaited_once()
        else:
            mock_cria_notif_individual_db.assert_awaited_once()

@pytest.mark.asyncio
async def test_cria_notificacao_orcamento_mais_votado():
    # Caso de Sucesso
    db = MagicMock()  # Mock do banco de dados
    pedido = MagicMock()
    pedido.PMID = 123
    pedido.RecursoComun_.Nome = "Piscina"

    # Mock para o tipo de processo
    with patch("services.notificacao_service.get_tipo_processo_id", return_value=99), \
            patch("services.notificacao_service.cria_notificacao_todos_utilizadores_db",
                  return_value=(True, "ok")) as mock_cria_notif_db:
        # Act (sucesso)
        result = await cria_notificacao_orcamento_mais_votado(db, pedido, "Orçamento A")

        # Assert (sucesso)
        assert result == (True, "ok")
        mock_cria_notif_db.assert_awaited_once()

    # Caso de Erro
    with patch("services.notificacao_service.get_tipo_processo_id", return_value=99), \
            patch("services.notificacao_service.cria_notificacao_todos_utilizadores_db",
                  side_effect=Exception("Erro ao criar notificação")):
        # Act / Assert (erro)
        with pytest.raises(HTTPException):
            await cria_notificacao_orcamento_mais_votado(db, pedido, "Orçamento A")

@pytest.mark.asyncio
async def test_cria_notificacao_conclusao_manutencao_recurso_comum():
    # Caso de Sucesso
    db = MagicMock()  # Mock do banco de dados
    manutencao = MagicMock()
    manutencao.PMID = 123
    manutencao.Fornecedor = "Fornecedor A"

    pedido = MagicMock()
    pedido.PMID = 123
    pedido.RecursoComun_.Nome = "Piscina"

    # Mock para as funções chamadas dentro da função
    with patch("services.notificacao_service.get_tipo_processo_id", return_value=99), \
            patch("services.notificacao_service.cria_notificacao_todos_utilizadores_db",
                  return_value=(True, "ok")) as mock_cria_notif_db, \
            patch("services.recurso_comum_service.obter_pedido_manutencao", return_value=pedido):
        # Act (sucesso)
        result = await cria_notificacao_conclusao_manutencao_recurso_comum(db, manutencao, MagicMock())

        # Assert (sucesso)
        assert result == (True, "ok")
        mock_cria_notif_db.assert_awaited_once()

    # Caso de Erro
    with patch("services.notificacao_service.get_tipo_processo_id", return_value=99), \
            patch("services.notificacao_service.cria_notificacao_todos_utilizadores_db",
                  side_effect=Exception("Erro ao criar notificação")), \
            patch("services.recurso_comum_service.obter_pedido_manutencao", return_value=None):
        # Act / Assert (erro)
        with pytest.raises(HTTPException):
            await cria_notificacao_conclusao_manutencao_recurso_comum(db, manutencao, MagicMock())

@pytest.mark.asyncio
async def test_notificacoes_insercao_e_anuncio_pedido_novo_recurso_comum():
    # Mock do banco de dados
    db = MagicMock()

    # Mock do pedido
    pedido = MagicMock(spec=PedidoNovoRecursoSchema)

    # Mock para o Utilizador_
    pedido.Utilizador_ = MagicMock()
    pedido.Utilizador_.UtilizadorID = 456

    # Definir os outros atributos mockados para o pedido
    pedido.PedidoNovoRecID = 123
    pedido.DataPedido = "2025-05-02"

    # Mock do tipo de processo
    with patch("services.notificacao_service.get_tipo_processo_id", return_value=99):
        # ------------------ Teste 1: Criar Notificação de Inserção de Pedido ------------------
        # Mock da função que cria a notificação para o admin
        with patch("services.notificacao_service.cria_notificacao_admin_db",
                   return_value=(True, "ok")) as mock_cria_notif_admin:
            # Caso de Sucesso (Inserção de Pedido)
            result = await cria_notificacao_insercao_pedido_novo_recurso_comum_service(db, pedido)

            # Assert (sucesso)
            assert result == (True, "ok")
            mock_cria_notif_admin.assert_awaited_once()

        # Caso de Erro (Inserção de Pedido)
        with patch("services.notificacao_service.cria_notificacao_admin_db",
                   side_effect=Exception("Erro ao criar notificação para o admin")):
            # Act / Assert (erro)
            with pytest.raises(HTTPException):
                await cria_notificacao_insercao_pedido_novo_recurso_comum_service(db, pedido)

        # ------------------ Teste 2: Criar Notificação de Anúncio de Compra ------------------
        # Mock da função que cria a notificação para todos os utilizadores
        with patch("services.notificacao_service.cria_notificacao_todos_utilizadores_db",
                   return_value=(True, "ok")) as mock_cria_notif_todos:
            # Caso de Sucesso (Anúncio de Compra)
            result = await cria_notificacao_anuncio_compra_novo_recurso_comum_service(db, pedido, "Orçamento A")

            # Assert (sucesso)
            assert result == (True, "ok")
            mock_cria_notif_todos.assert_awaited_once()

        # Caso de Erro (Anúncio de Compra)
        with patch("services.notificacao_service.cria_notificacao_todos_utilizadores_db",
                   side_effect=Exception("Erro ao criar notificação para todos os utilizadores")):
            # Act / Assert (erro)
            with pytest.raises(HTTPException):
                await cria_notificacao_anuncio_compra_novo_recurso_comum_service(db, pedido, "Orçamento A")

@pytest.mark.asyncio
async def test_notificacoes_pedido_reserva():
    # Mock do banco de dados
    db = MagicMock()

    # Mock do pedido
    pedido = MagicMock(spec=PedidoReserva)
    pedido.PedidoResevaID = 123
    pedido.Recurso_.Nome = "Recurso X"
    pedido.Recurso_.UtilizadorID = 456
    pedido.Utilizador_.NomeUtilizador = "José Silva"
    pedido.Utilizador_.UtilizadorID = 789
    pedido.DataInicio = "2025-05-02"
    pedido.DataFim = "2025-05-05"

    # Mock do reserva
    reserva = MagicMock(spec=Reserva)
    reserva.ReservaID = 123
    reserva.PedidoResevaID=pedido.PedidoResevaID
    reserva.ConfirmarCaucaoDono = True
    reserva.ConfirmarCaucaoVizinho = True
    reserva.RecursoEntregueDono = True
    reserva.RecursoEntregueVizinho = True
    reserva.DevolucaoCaucao = True
    reserva.EstadoRecurso = True
    reserva.PedidoReserva_ = pedido


    # Mock da função de get_tipo_processo_id
    with patch("services.notificacao_service.get_tipo_processo_id", return_value=99):
        # ------------------- Teste 1: Notificação de Recebimento de Pedido -------------------
        with patch("services.notificacao_service.cria_notificacao_individual_db",
                   return_value=(True, "ok")) as mock_cria_notif:
            # Caso de Sucesso
            result = await cria_notificacao_recebimento_pedido_reserva(db, pedido)
            assert result == (True, "ok")
            mock_cria_notif.assert_awaited_once()

        with patch("services.notificacao_service.cria_notificacao_individual_db",
                   side_effect=Exception("Erro ao criar notificação")):
            # Caso de Erro
            with pytest.raises(Exception):
                await cria_notificacao_recebimento_pedido_reserva(db, pedido)

        # ------------------- Teste 2: Notificação de Recusa de Pedido -------------------
        motivo_recusa = "Recurso não disponível"
        with patch("services.notificacao_service.cria_notificacao_individual_db",
                   return_value=(True, "ok")) as mock_cria_notif:
            # Caso de Sucesso
            result = await cria_notificacao_recusa_pedido_reserva(db, pedido, motivo_recusa)
            assert result == (True, "ok")
            mock_cria_notif.assert_awaited_once()

        with patch("services.notificacao_service.cria_notificacao_individual_db",
                   side_effect=Exception("Erro ao criar notificação")):
            # Caso de Erro
            with pytest.raises(HTTPException):
                await cria_notificacao_recusa_pedido_reserva(db, pedido, motivo_recusa)

        # ------------------- Teste 3: Notificação de Aceitação de Pedido -------------------
        with patch("services.notificacao_service.cria_notificacao_individual_db",
                   return_value=(True, "ok")) as mock_cria_notif:
            # Caso de Sucesso
            result = await cria_notificacao_aceitacao_pedido_reserva(db, pedido)
            assert result == (True, "ok")
            mock_cria_notif.assert_awaited_once()

        with patch("services.notificacao_service.cria_notificacao_individual_db",
                   side_effect=Exception("Erro ao criar notificação")):
            # Caso de Erro
            with pytest.raises(HTTPException):
                await cria_notificacao_aceitacao_pedido_reserva(db, pedido)

        # ------------------- Teste 4: Notificação de Caução Devolvida -------------------
        with patch("services.notificacao_service.cria_notificacao_individual_db",
                   return_value=(True, "ok")) as mock_cria_notif:
            # Caso de Sucesso
            result = await cria_notificacao_caucao_devolucao_pedido_reserva(db, reserva, reserva.ReservaID)
            assert result == (True, "ok")
            mock_cria_notif.assert_awaited_once()

        with patch("services.notificacao_service.cria_notificacao_individual_db",
                   side_effect=Exception("Erro ao criar notificação")):
            # Caso de Erro
            with pytest.raises(HTTPException):
                await cria_notificacao_caucao_devolucao_pedido_reserva(db, reserva, reserva.ReservaID)

        # ------------------- Teste 5: Notificação de Caução Não Devolvida -------------------
        justificativa = "Recurso danificado"
        with patch("services.notificacao_service.cria_notificacao_individual_db",
                   return_value=(True, "ok")) as mock_cria_notif:
            # Caso de Sucesso
            result = await cria_notificacao_nao_caucao_devolucao_pedido_reserva(db, reserva, reserva.ReservaID, justificativa)
            assert result == (True, "ok")
            mock_cria_notif.assert_awaited_once()

        with patch("services.notificacao_service.cria_notificacao_individual_db",
                   side_effect=Exception("Erro ao criar notificação")):
            # Caso de Erro
            with pytest.raises(HTTPException):
                await cria_notificacao_nao_caucao_devolucao_pedido_reserva(db, reserva, reserva.ReservaID, justificativa)

if __name__ == '__main__':
    unittest.main()
