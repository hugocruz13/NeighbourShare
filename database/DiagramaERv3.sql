create table EstadoDevolucao (
  EDID   int identity not null, 
  [Desc] varchar(255) not null, 
  primary key (EDID));
create table TipoProcesso (
  TipoProcID int identity not null, 
  [Desc]     varchar(255) not null, 
  primary key (TipoProcID));
create table Orcamento (
  OrcamentoID int identity not null, 
  Fornecedor  varchar(255) not null, 
  Valor       decimal(19, 0) not null, 
  [Desc]      varchar(255) not null, 
  primary key (OrcamentoID));
create table EstadoPedidoNovoRecurso (
  EstadoPedNovoRecID int identity not null, 
  [Desc]             varchar(255) not null, 
  primary key (EstadoPedNovoRecID));
create table PedidoNovoRecurso (
  PedidoNovoRecID    int identity not null, 
  UtilizadorID       int not null, 
  [Desc]             varchar(255) not null, 
  DataPedido         date not null, 
  EstadoPedNovoRecID int not null, 
  primary key (PedidoNovoRecID));
create table NotificacaoUser (
  NotificacaoID int not null, 
  UtilizadorID  int not null, 
  primary key (NotificacaoID, 
  UtilizadorID));
create table Voto (
  VotacaoID    int not null, 
  UtilizadorID int not null, 
  EscolhaVoto  varchar(255) not null, 
  DataVoto     datetime not null, 
  primary key (VotacaoID, 
  UtilizadorID));
create table Votacao (
  VotacaoID  int identity not null, 
  Titulo     varchar(255) not null, 
  Descricao  varchar(255) not null, 
  DataInicio date not null, 
  DataFim    date not null, 
  primary key (VotacaoID));
create table EstadoManutencao (
  EstadoManuID int identity not null, 
  [Desc]       varchar(255) not null, 
  primary key (EstadoManuID));
create table EntidadeExterna (
  EntidadeID    int identity not null, 
  Especialidade varchar(255) not null, 
  Contacto      int not null, 
  Email         varchar(255) not null, 
  Nome          varchar(255) not null, 
  primary key (EntidadeID));
create table EstadoPedidoManutencao (
  EstadoPedManuID int identity not null, 
  [Desc]          varchar(255) not null, 
  primary key (EstadoPedManuID));
create table RecursoComun (
  RecComumID int identity not null, 
  Nome       varchar(255) not null, 
  [Desc]     varchar(255) not null, 
  primary key (RecComumID));
create table Notificacao (
  NotificacaoID int identity not null, 
  Mensagem      varchar(255) not null, 
  DataHora      datetime not null, 
  ProcessoID    int not null, 
  Estado        bit not null, 
  TipoProcID    int not null, 
  primary key (NotificacaoID));
create table Reserva (
  ReservaID              int identity not null, 
  PedidoResevaID         int not null, 
  ConfirmarCaucaoDono    bit not null, 
  ConfirmarCaucaoVizinho bit not null, 
  RecursoEntregueDono    bit not null, 
  RecursoEntregueVizinho bit not null, 
  DevolucaoCaucao        bit not null, 
  EstadoRecurso          bit not null, 
  primary key (ReservaID));
create table Disponibilidade (
  DispID int identity not null, 
  [Desc] varchar(255) not null, 
  primary key (DispID));
create table Manutencao (
  ManutencaoID   int identity not null, 
  PMID           int not null, 
  EntidadeID     int not null, 
  DataManutencao date not null, 
  DescMan        varchar(255) not null, 
  EstadoManuID   int not null, 
  primary key (ManutencaoID));
create table PedidoManutencao (
  PMID            int identity not null, 
  UtilizadorID    int not null, 
  RecComumID      int not null, 
  DescPedido      varchar(255) not null, 
  DataPedido      date not null, 
  EstadoPedManuID int not null, 
  primary key (PMID));
create table EstadoPedidoReserva (
  EstadoID int identity not null, 
  [Desc]   varchar(255) not null, 
  primary key (EstadoID));
create table PedidoReserva (
  PedidoResevaID int identity not null, 
  UtilizadorID   int not null, 
  RecursoID      int not null, 
  DataInicio     date not null, 
  DataFim        date not null, 
  EstadoID       int not null, 
  primary key (PedidoResevaID));
create table Categoria (
  CatID  int identity not null, 
  [Desc] varchar(255) not null, 
  primary key (CatID));
create table TipoUtilizador (
  TUID   int identity not null, 
  DescTU varchar(255) not null, 
  primary key (TUID));
create table Recurso (
  RecursoID    int identity not null, 
  Nome         varchar(50) not null, 
  DescRecurso  varchar(255) not null, 
  Caucao       decimal(19, 0) not null, 
  Imagem       image not null, 
  UtilizadorID int not null, 
  DispID       int not null, 
  CatID        int not null, 
  primary key (RecursoID));
create table Utilizador (
  UtilizadorID   int identity not null, 
  NomeUtilizador varchar(255) not null, 
  DataNasc       date not null, 
  Contacto       int not null, 
  Email          varchar(255) not null unique, 
  PasswordHash   varchar(64) not null, 
  Salt           varchar(32) not null, 
  Foto           image not null, 
  TUID           int not null, 
  primary key (UtilizadorID));
create table OrcamentoPedidoNovoRecurso (
  OrcamentoID     int not null, 
  PedidoNovoRecID int not null, 
  primary key (OrcamentoID, 
  PedidoNovoRecID));
create table OrcamentoPedidoManutencao (
  OrcamentoID  int not null, 
  ManutencaoID int not null, 
  primary key (OrcamentoID, 
  ManutencaoID));
create table VotacaoPedidoNovoRecurso (
  TipoVotacao     int not null, 
  VotacaoID       int not null, 
  PedidoNovoRecID int not null, 
  primary key (TipoVotacao, 
  VotacaoID, 
  PedidoNovoRecID));
create table VotacaoOrcamentoManutencao (
  VotacaoID    int not null, 
  ManutencaoID int not null, 
  primary key (VotacaoID, 
  ManutencaoID));
alter table PedidoNovoRecurso add constraint FKPedidoNovo687404 foreign key (EstadoPedNovoRecID) references EstadoPedidoNovoRecurso (EstadoPedNovoRecID);
alter table Voto add constraint FKVoto757754 foreign key (VotacaoID) references Votacao (VotacaoID);
alter table NotificacaoUser add constraint FKNotificaca868180 foreign key (NotificacaoID) references Notificacao (NotificacaoID);
alter table Notificacao add constraint FKNotificaca853595 foreign key (TipoProcID) references TipoProcesso (TipoProcID);
alter table Manutencao add constraint FKManutencao947029 foreign key (EntidadeID) references EntidadeExterna (EntidadeID);
alter table Manutencao add constraint FKManutencao654470 foreign key (EstadoManuID) references EstadoManutencao (EstadoManuID);
alter table Manutencao add constraint FKManutencao23106 foreign key (PMID) references PedidoManutencao (PMID);
alter table PedidoManutencao add constraint FKPedidoManu235529 foreign key (RecComumID) references RecursoComun (RecComumID);
alter table PedidoManutencao add constraint FKPedidoManu183438 foreign key (EstadoPedManuID) references EstadoPedidoManutencao (EstadoPedManuID);
alter table [Reserva ] add constraint [FKReserva 41673] foreign key (PedidoResevaID) references PedidoReserva (PedidoResevaID);
alter table PedidoReserva add constraint FKPedidoRese354298 foreign key (EstadoID) references EstadoPedidoReserva (EstadoID);
alter table PedidoReserva add constraint FKPedidoRese183537 foreign key (RecursoID) references Recurso (RecursoID);
alter table Recurso add constraint FKRecurso462257 foreign key (DispID) references Disponibilidade (DispID);
alter table Recurso add constraint FKRecurso936704 foreign key (CatID) references Categoria (CatID);
alter table Recurso add constraint FKRecurso905396 foreign key (UtilizadorID) references Utilizador (UtilizadorID);
alter table PedidoReserva add constraint FKPedidoRese738683 foreign key (UtilizadorID) references Utilizador (UtilizadorID);
alter table PedidoManutencao add constraint FKPedidoManu652837 foreign key (UtilizadorID) references Utilizador (UtilizadorID);
alter table Voto add constraint FKVoto117230 foreign key (UtilizadorID) references Utilizador (UtilizadorID);
alter table NotificacaoUser add constraint FKNotificaca496296 foreign key (UtilizadorID) references Utilizador (UtilizadorID);
alter table PedidoNovoRecurso add constraint FKPedidoNovo924624 foreign key (UtilizadorID) references Utilizador (UtilizadorID);
alter table Utilizador add constraint FKUtilizador842840 foreign key (TUID) references TipoUtilizador (TUID);
alter table OrcamentoPedidoNovoRecurso add constraint FKOrcamentoP299373 foreign key (OrcamentoID) references Orcamento (OrcamentoID);
alter table OrcamentoPedidoNovoRecurso add constraint FKOrcamentoP11081 foreign key (PedidoNovoRecID) references PedidoNovoRecurso (PedidoNovoRecID);
alter table OrcamentoPedidoManutencao add constraint FKOrcamentoP892124 foreign key (OrcamentoID) references Orcamento (OrcamentoID);
alter table OrcamentoPedidoManutencao add constraint FKOrcamentoP946778 foreign key (ManutencaoID) references Manutencao (ManutencaoID);
alter table VotacaoPedidoNovoRecurso add constraint FKVotacaoPed984472 foreign key (VotacaoID) references Votacao (VotacaoID);
alter table VotacaoPedidoNovoRecurso add constraint FKVotacaoPed723238 foreign key (PedidoNovoRecID) references PedidoNovoRecurso (PedidoNovoRecID);
alter table VotacaoOrcamentoManutencao add constraint FKVotacaoOrc131595 foreign key (VotacaoID) references Votacao (VotacaoID);
alter table VotacaoOrcamentoManutencao add constraint FKVotacaoOrc476843 foreign key (ManutencaoID) references Manutencao (ManutencaoID);
