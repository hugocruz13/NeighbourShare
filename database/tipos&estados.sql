/*Tipo de processo associado à tabela notificações*/

INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Aquisição');
INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Manutenção');
INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Reserva');
INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Votação');

/*Estado Pedido Novo Recurso*/

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

/*Estado Pedido de Manutenção de um recurso comum*/

INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao)
VALUES ('Em análise');

INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao)
VALUES ('Aprovado para execução interna');

INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao)
<<<<<<< HEAD
VALUES ('Em negociação com entidades externas');

INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao)
VALUES ('Em votação');
=======
VALUES ('Aprovado para execução externa');
>>>>>>> origin/votaÃ§Ã£o

INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao)
VALUES ('Rejeitado');


<<<<<<< HEAD
/*Estado Manutenção de um recurso comum*/


INSERT INTO EstadoManutencao (DescEstadoManutencao)
VALUES ('Em progresso');

INSERT INTO EstadoManutencao (DescEstadoManutencao)
VALUES ('Concluída');


=======
>>>>>>> origin/votaÃ§Ã£o
/*Tipo Utilizador*/

INSERT INTO TipoUtilizador (DescTU) VALUES ('Residente')
INSERT INTO TipoUtilizador (DescTU) VALUES ('Gestor')

/*Disponibilidade do recurso*/

INSERT INTO Disponibilidade (DescDisponibilidade) VALUES ('Disponível')
INSERT INTO Disponibilidade (DescDisponibilidade) VALUES ('Indisponível')

/*Categoria de Recursos*/

INSERT INTO Categoria (DescCategoria) VALUES ('Lazer')
INSERT INTO Categoria (DescCategoria) VALUES ('Tecnologia')
INSERT INTO Categoria (DescCategoria) VALUES ('Ferramentas')
INSERT INTO Categoria (DescCategoria) VALUES ('Cozinha')
INSERT INTO Categoria (DescCategoria) VALUES ('Outros')

/* Estado Pedido Reserva */

INSERT INTO EstadoPedidoReserva (DescEstadoPedidoReserva) VALUES ('Em análise')
INSERT INTO EstadoPedidoReserva (DescEstadoPedidoReserva) VALUES ('Aprovado')
INSERT INTO EstadoPedidoReserva (DescEstadoPedidoReserva) VALUES ('Rejeitado')




