USE NeighbourShare

IF NOT EXISTS (SELECT 1 FROM TipoProcesso WHERE DescTipoProcesso = 'Aquisição') INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Aquisição');
IF NOT EXISTS (SELECT 1 FROM TipoProcesso WHERE DescTipoProcesso = 'Manutenção') INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Manutenção');
IF NOT EXISTS (SELECT 1 FROM TipoProcesso WHERE DescTipoProcesso = 'Reserva') INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Reserva');
IF NOT EXISTS (SELECT 1 FROM TipoProcesso WHERE DescTipoProcesso = 'Votação') INSERT INTO TipoProcesso (DescTipoProcesso) VALUES ('Votação');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoNovoRecurso WHERE DescEstadoPedidoNovoRecurso = 'Pendente')
INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso) VALUES ('Pendente');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoNovoRecurso WHERE DescEstadoPedidoNovoRecurso = 'Em votação')
INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso) VALUES ('Em votação');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoNovoRecurso WHERE DescEstadoPedidoNovoRecurso = 'Rejeitado')
INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso) VALUES ('Rejeitado');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoNovoRecurso WHERE DescEstadoPedidoNovoRecurso = 'Aprovado para orçamentação')
INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso) VALUES ('Aprovado para orçamentação');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoNovoRecurso WHERE DescEstadoPedidoNovoRecurso = 'Rejeitado após orçamentação')
INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso) VALUES ('Rejeitado após orçamentação');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoNovoRecurso WHERE DescEstadoPedidoNovoRecurso = 'Aprovado para compra')
INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso) VALUES ('Aprovado para compra');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoNovoRecurso WHERE DescEstadoPedidoNovoRecurso = 'Concluído')
INSERT INTO EstadoPedidoNovoRecurso (DescEstadoPedidoNovoRecurso) VALUES ('Concluído');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoManutencao WHERE DescEstadoPedidoManutencao = 'Em análise')
INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao) VALUES ('Em análise');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoManutencao WHERE DescEstadoPedidoManutencao = 'Aprovado para execuçãoo interna')
INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao) VALUES ('Aprovado para execuçãoo interna');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoManutencao WHERE DescEstadoPedidoManutencao = 'Aprovado para execução externa')
INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao) VALUES ('Aprovado para execução externa');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoManutencao WHERE DescEstadoPedidoManutencao = 'Rejeitado')
INSERT INTO EstadoPedidoManutencao (DescEstadoPedidoManutencao) VALUES ('Rejeitado');

IF NOT EXISTS (SELECT 1 FROM TipoUtilizador WHERE DescTU = 'admin') INSERT INTO TipoUtilizador (DescTU) VALUES ('admin');
IF NOT EXISTS (SELECT 1 FROM TipoUtilizador WHERE DescTU = 'residente') INSERT INTO TipoUtilizador (DescTU) VALUES ('residente');
IF NOT EXISTS (SELECT 1 FROM TipoUtilizador WHERE DescTU = 'gestor') INSERT INTO TipoUtilizador (DescTU) VALUES ('gestor');

IF NOT EXISTS (SELECT 1 FROM Disponibilidade WHERE DescDisponibilidade = 'Disponível') INSERT INTO Disponibilidade (DescDisponibilidade) VALUES ('Disponível');
IF NOT EXISTS (SELECT 1 FROM Disponibilidade WHERE DescDisponibilidade = 'Indisponível') INSERT INTO Disponibilidade (DescDisponibilidade) VALUES ('Indisponível');

IF NOT EXISTS (SELECT 1 FROM Categoria WHERE DescCategoria = 'Lazer') INSERT INTO Categoria (DescCategoria) VALUES ('Lazer');
IF NOT EXISTS (SELECT 1 FROM Categoria WHERE DescCategoria = 'Tecnologia') INSERT INTO Categoria (DescCategoria) VALUES ('Tecnologia');
IF NOT EXISTS (SELECT 1 FROM Categoria WHERE DescCategoria = 'Ferramentas') INSERT INTO Categoria (DescCategoria) VALUES ('Ferramentas');
IF NOT EXISTS (SELECT 1 FROM Categoria WHERE DescCategoria = 'Cozinha') INSERT INTO Categoria (DescCategoria) VALUES ('Cozinha');
IF NOT EXISTS (SELECT 1 FROM Categoria WHERE DescCategoria = 'Outros') INSERT INTO Categoria (DescCategoria) VALUES ('Outros');

IF NOT EXISTS (SELECT 1 FROM EstadoPedidoReserva WHERE DescEstadoPedidoReserva = 'Em análise') INSERT INTO EstadoPedidoReserva (DescEstadoPedidoReserva) VALUES ('Em análise');
IF NOT EXISTS (SELECT 1 FROM EstadoPedidoReserva WHERE DescEstadoPedidoReserva = 'Aprovado') INSERT INTO EstadoPedidoReserva (DescEstadoPedidoReserva) VALUES ('Aprovado');
IF NOT EXISTS (SELECT 1 FROM EstadoPedidoReserva WHERE DescEstadoPedidoReserva = 'Rejeitado') INSERT INTO EstadoPedidoReserva (DescEstadoPedidoReserva) VALUES ('Rejeitado');

/* INSERT INTO EstadoManutencao (DescEstadoManutencao) VALUES ('Aguardar entidade externa'); */
IF NOT EXISTS (SELECT 1 FROM EstadoManutencao WHERE DescEstadoManutencao = 'Em curso') INSERT INTO EstadoManutencao (DescEstadoManutencao) VALUES ('Em curso');
IF NOT EXISTS (SELECT 1 FROM EstadoManutencao WHERE DescEstadoManutencao = 'Concluído') INSERT INTO EstadoManutencao (DescEstadoManutencao) VALUES ('Concluído');
