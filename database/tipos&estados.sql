USE NeighbourShare

INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Aquisição');
INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Manutenção');
INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Reserva');
INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Votação');

INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso)
VALUES ('Pendente');

INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso)
VALUES ('Em votação');

INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso)
VALUES ('Rejeitado');

INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso)
VALUES ('Aprovado para orçamentação');

INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso)
VALUES ('Rejeitado após orçamentação');

INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso)
VALUES ('Aprovado para compra');

INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso)
VALUES ('Concluído');

INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao)
VALUES ('Em análise');

INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao)
VALUES ('Aprovado para execuçãoo interna');

INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao)
VALUES ('Aprovado para execução externa');

INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao)
VALUES ('Rejeitado');

INSERT INTO TipoUtilizador (DescTU) VALUES ('admin')
INSERT INTO TipoUtilizador (DescTU) VALUES ('residente')
INSERT INTO TipoUtilizador (DescTU) VALUES ('gestor')

INSERT INTO Disponibilidade (DescDisponibilidade) VALUES ('Disponível')
INSERT INTO Disponibilidade (DescDisponibilidade) VALUES ('Indisponível')

INSERT INTO Categoria (DescCategoria) VALUES ('Lazer')
INSERT INTO Categoria (DescCategoria) VALUES ('Tecnologia')
INSERT INTO Categoria (DescCategoria) VALUES ('Ferramentas')
INSERT INTO Categoria (DescCategoria) VALUES ('Cozinha')
INSERT INTO Categoria (DescCategoria) VALUES ('Outros')

INSERT INTO EstadoPedidoReserva (DescEstadoPedidoReserva) VALUES ('Em análise')
INSERT INTO EstadoPedidoReserva (DescEstadoPedidoReserva) VALUES ('Aprovado')
INSERT INTO EstadoPedidoReserva (DescEstadoPedidoReserva) VALUES ('Rejeitado')

/*INSERT INTO EstadoManutencao (DescEstadoManutencao) VALUES ('Aguardar entidade externa')*/
INSERT INTO EstadoManutencao (DescEstadoManutencao) VALUES ('Em curso')
INSERT INTO EstadoManutencao (DescEstadoManutencao) VALUES ('Concluído')