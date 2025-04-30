import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from unittest import mock
import unittest
from datetime import date, timedelta, datetime
import asyncio
from pydantic import ValidationError
from fastapi import HTTPException

from schemas.votacao_schema import TipoVotacao

"""

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ANTES DE EXECUTAR O TESTE, VERIFIQUE SE OS IDs DEFINIDOS NO CÓDIGO COMO
O DO UTILIZADOR, ESTÃO A PAR DO QUE ESTÁ NA BASE DE DADOS.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""
from schemas.recurso_comum_schema import PedidoNovoRecursoSchemaCreate
from services.recurso_comum_service import inserir_pedido_novo_recurso_service
from db.repository import recurso_comum_repo
from services import notificacao_service

class TestInserirPedidoNovoRecursoService:

    @pytest.mark.asyncio
    async def test_inserir_pedido_novo_recurso_service_sucesso(self):
        """
        Testa se a função inserir_pedido_novo_recurso_service insere um pedido com sucesso
        e cria a notificação correspondente.
        """
        # Arrange
        # Mock da sessão do banco de dados
        db_mock = MagicMock()

        # Dados de um pedido válido
        pedido_valido = PedidoNovoRecursoSchemaCreate(
            UtilizadorID=1,
            DescPedidoNovoRecurso="Solicitação de novo monitor para o departamento de design",
            DataPedido=date.today(),
            EstadoPedNovoRecID=1
        )

        # Usar model_dump() em vez de dict()
        mock_pedido_retorno = {"id": 1, **pedido_valido.model_dump()}
        recurso_comum_repo.inserir_pedido_novo_recurso_db = AsyncMock(
            return_value=("Pedido de novo recurso inserido com sucesso!", mock_pedido_retorno)
        )

        # Mock do serviço de notificação
        notificacao_service.cria_notificacao_insercao_pedido_novo_recurso_comum_service = AsyncMock(
            return_value="Inserção de notificações para os admins realizada com sucesso!"
        )

        # Act
        msg_sucesso, msg_noti = await inserir_pedido_novo_recurso_service(db_mock, pedido_valido)

        # Assert
        assert msg_sucesso == "Pedido de novo recurso inserido com sucesso!"
        assert msg_noti == "Inserção de notificações para os admins realizada com sucesso!"
        recurso_comum_repo.inserir_pedido_novo_recurso_db.assert_called_once_with(db_mock, pedido_valido)
        notificacao_service.cria_notificacao_insercao_pedido_novo_recurso_comum_service.assert_called_once_with(
            db_mock, mock_pedido_retorno
        )

    @pytest.mark.asyncio
    async def test_inserir_pedido_novo_recurso_service_erro(self):
        """
        Testa se a função inserir_pedido_novo_recurso_service trata corretamente
        uma exceção gerada durante a inserção do pedido.
        """
        # Criando os mocks
        mock_repo = AsyncMock()
        mock_notificacao = AsyncMock()

        # Configurando o mock para lançar uma exceção
        erro_mensagem = "Erro ao inserir pedido no banco de dados"
        mock_repo.inserir_pedido_novo_recurso_db = AsyncMock(
            side_effect=Exception(erro_mensagem)
        )

        # Injetando os mocks
        with patch('services.recurso_comum_service.recurso_comum_repo', mock_repo), \
                patch('services.recurso_comum_service.notificacao_service', mock_notificacao):

            from services.recurso_comum_service import inserir_pedido_novo_recurso_service

            # Arrange
            db_mock = MagicMock()
            pedido_valido = MagicMock()

            # Act/Assert
            with pytest.raises(HTTPException) as excinfo:
                await inserir_pedido_novo_recurso_service(db_mock, pedido_valido)

            # Verifica se a exceção HTTP tem o status code e a mensagem corretos
            assert excinfo.value.status_code == 500
            assert excinfo.value.detail == erro_mensagem

            # Verifica se a função do repositório foi chamada
            mock_repo.inserir_pedido_novo_recurso_db.assert_called_once_with(db_mock, pedido_valido)

            # Verifica se a função de notificação NÃO foi chamada
            mock_notificacao.cria_notificacao_insercao_pedido_novo_recurso_comum_service.assert_not_called()

    @pytest.mark.asyncio
    def test_inserir_pedido_novo_recurso_schema_validacao(self):
        """
        Testa a validação do schema PedidoNovoRecursoSchemaCreate
        """

        # Teste de validação da descrição muito curta
        with pytest.raises(ValidationError) as excinfo:
            PedidoNovoRecursoSchemaCreate(
                UtilizadorID=1,
                DescPedidoNovoRecurso="Curt",  # Menos de 5 caracteres
                DataPedido=date.today(),
                EstadoPedNovoRecID=1
            )
        errors = excinfo.value.errors()
        assert any(
            err["loc"] == ("DescPedidoNovoRecurso",) and
            "at least 5 characters" in err["msg"]
            for err in errors
        )

        # Teste de validação de ID inválido
        with pytest.raises(ValidationError) as excinfo:
            PedidoNovoRecursoSchemaCreate(
                UtilizadorID=0,  # ID deve ser maior que 0
                DescPedidoNovoRecurso="Descrição válida do pedido",
                DataPedido=date.today(),
                EstadoPedNovoRecID=1
            )
        errors = excinfo.value.errors()
        assert any(
            err["loc"] == ("UtilizadorID",) and
            "greater than 0" in err["msg"]
            for err in errors
        )

if __name__ == '__main__':
    unittest.main()

