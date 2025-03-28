from typing import List, Optional

from sqlalchemy import Boolean, Column, DECIMAL, Date, DateTime, ForeignKeyConstraint, Identity, Index, Integer, PrimaryKeyConstraint, String, Table
from sqlalchemy.dialects.mssql import IMAGE
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Categoria(Base):
    __tablename__ = 'Categoria'
    __table_args__ = (
        PrimaryKeyConstraint('CatID', name='PK__Categori__6A1C8ADADA848899'),
    )

    CatID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    DescCategoria: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Recurso: Mapped[List['Recurso']] = relationship('Recurso', back_populates='Categoria_')


class Disponibilidade(Base):
    __tablename__ = 'Disponibilidade'
    __table_args__ = (
        PrimaryKeyConstraint('DispID', name='PK__Disponib__1682E8116F6522ED'),
    )

    DispID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    DescDisponibilidade: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Recurso: Mapped[List['Recurso']] = relationship('Recurso', back_populates='Disponibilidade_')


class EntidadeExterna(Base):
    __tablename__ = 'EntidadeExterna'
    __table_args__ = (
        PrimaryKeyConstraint('EntidadeID', name='PK__Entidade__6894D27512C1B7A3'),
    )

    EntidadeID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Especialidade: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    Contacto: Mapped[int] = mapped_column(Integer)
    Email: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    Nome: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Manutencao: Mapped[List['Manutencao']] = relationship('Manutencao', back_populates='EntidadeExterna_')


class EstadoDevolucao(Base):
    __tablename__ = 'EstadoDevolucao'
    __table_args__ = (
        PrimaryKeyConstraint('EDID', name='PK__EstadoDe__277517575E7213DD'),
    )

    EDID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Desc: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))


class EstadoManutencao(Base):
    __tablename__ = 'EstadoManutencao'
    __table_args__ = (
        PrimaryKeyConstraint('EstadoManuID', name='PK__EstadoMa__6A784FD4C18D4EAE'),
    )

    EstadoManuID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    DescEstadoManutencao: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Manutencao: Mapped[List['Manutencao']] = relationship('Manutencao', back_populates='EstadoManutencao_')


class EstadoPedidoManutencao(Base):
    __tablename__ = 'EstadoPedidoManutencao'
    __table_args__ = (
        PrimaryKeyConstraint('EstadoPedManuID', name='PK__EstadoPe__0010CC67163A3E34'),
    )

    EstadoPedManuID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    DescEstadoPedidoManutencao: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    PedidoManutencao: Mapped[List['PedidoManutencao']] = relationship('PedidoManutencao', back_populates='EstadoPedidoManutencao_')


class EstadoPedidoNovoRecurso(Base):
    __tablename__ = 'EstadoPedidoNovoRecurso'
    __table_args__ = (
        PrimaryKeyConstraint('EstadoPedNovoRecID', name='PK__EstadoPe__4A23F621917F901B'),
    )

    EstadoPedNovoRecID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    DescEstadoPedidoNovoRecurso: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    PedidoNovoRecurso: Mapped[List['PedidoNovoRecurso']] = relationship('PedidoNovoRecurso', back_populates='EstadoPedidoNovoRecurso_')


class EstadoPedidoReserva(Base):
    __tablename__ = 'EstadoPedidoReserva'
    __table_args__ = (
        PrimaryKeyConstraint('EstadoID', name='PK__EstadoPe__FEF86B60A7E5262A'),
    )

    EstadoID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    DescEstadoPedidoReserva: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    PedidoReserva: Mapped[List['PedidoReserva']] = relationship('PedidoReserva', back_populates='EstadoPedidoReserva_')


class Orcamento(Base):
    __tablename__ = 'Orcamento'
    __table_args__ = (
        PrimaryKeyConstraint('OrcamentoID', name='PK__Orcament__4E96F759862E0F70'),
    )

    OrcamentoID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Fornecedor: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    Valor: Mapped[decimal.Decimal] = mapped_column(DECIMAL(19, 0))
    DescOrcamento: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    PedidoNovoRecurso: Mapped[List['PedidoNovoRecurso']] = relationship('PedidoNovoRecurso', secondary='OrcamentoPedidoNovoRecurso', back_populates='Orcamento_')
    Manutencao: Mapped[List['Manutencao']] = relationship('Manutencao', secondary='OrcamentoPedidoManutencao', back_populates='Orcamento_')


class RecursoComun(Base):
    __tablename__ = 'RecursoComun'
    __table_args__ = (
        PrimaryKeyConstraint('RecComumID', name='PK__RecursoC__0691E1D69D00824B'),
    )

    RecComumID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Nome: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    DescRecursoComum: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    PedidoManutencao: Mapped[List['PedidoManutencao']] = relationship('PedidoManutencao', back_populates='RecursoComun_')


class TipoProcesso(Base):
    __tablename__ = 'TipoProcesso'
    __table_args__ = (
        PrimaryKeyConstraint('TipoProcID', name='PK__TipoProc__D86DF0CCAC223E2F'),
    )

    TipoProcID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    DescTipoProcesso: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Notificacao: Mapped[List['Notificacao']] = relationship('Notificacao', back_populates='TipoProcesso_')


class TipoUtilizador(Base):
    __tablename__ = 'TipoUtilizador'
    __table_args__ = (
        PrimaryKeyConstraint('TUID', name='PK__TipoUtil__81338C4E090D4652'),
    )

    TUID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    DescTU: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Utilizador: Mapped[List['Utilizador']] = relationship('Utilizador', back_populates='TipoUtilizador_')


class Votacao(Base):
    __tablename__ = 'Votacao'
    __table_args__ = (
        PrimaryKeyConstraint('VotacaoID', name='PK__Votacao__F4DCDDBD37B4A8ED'),
    )

    VotacaoID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Titulo: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    Descricao: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    DataInicio: Mapped[datetime.date] = mapped_column(Date)
    DataFim: Mapped[datetime.date] = mapped_column(Date)

    Voto: Mapped[List['Voto']] = relationship('Voto', back_populates='Votacao_')
    Manutencao: Mapped[List['Manutencao']] = relationship('Manutencao', secondary='VotacaoOrcamentoManutencao', back_populates='Votacao_')
    VotacaoPedidoNovoRecurso: Mapped[List['VotacaoPedidoNovoRecurso']] = relationship('VotacaoPedidoNovoRecurso', back_populates='Votacao_')


class Notificacao(Base):
    __tablename__ = 'Notificacao'
    __table_args__ = (
        ForeignKeyConstraint(['TipoProcID'], ['TipoProcesso.TipoProcID'], name='FKNotificaca853595'),
        PrimaryKeyConstraint('NotificacaoID', name='PK__Notifica__FB9B785C6B7A8853')
    )

    NotificacaoID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Mensagem: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    DataHora: Mapped[datetime.datetime] = mapped_column(DateTime)
    ProcessoID: Mapped[int] = mapped_column(Integer)
    Estado: Mapped[bool] = mapped_column(Boolean)
    TipoProcID: Mapped[int] = mapped_column(Integer)

    TipoProcesso_: Mapped['TipoProcesso'] = relationship('TipoProcesso', back_populates='Notificacao')
    Utilizador: Mapped[List['Utilizador']] = relationship('Utilizador', secondary='NotificacaoUser', back_populates='Notificacao_')


class Utilizador(Base):
    __tablename__ = 'Utilizador'
    __table_args__ = (
        ForeignKeyConstraint(['TUID'], ['TipoUtilizador.TUID'], name='FKUtilizador842840'),
        PrimaryKeyConstraint('UtilizadorID', name='PK__Utilizad__90F8E1C820CD9F91'),
        Index('UQ__Utilizad__A9D10534C0B7D055', 'Email', unique=True)
    )

    UtilizadorID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    NomeUtilizador: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    DataNasc: Mapped[datetime.date] = mapped_column(Date)
    Contacto: Mapped[int] = mapped_column(Integer)
    Email: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PasswordHash: Mapped[str] = mapped_column(String(64, 'SQL_Latin1_General_CP1_CI_AS'))
    Salt: Mapped[str] = mapped_column(String(32, 'SQL_Latin1_General_CP1_CI_AS'))
    TUID: Mapped[int] = mapped_column(Integer)

    Notificacao_: Mapped[List['Notificacao']] = relationship('Notificacao', secondary='NotificacaoUser', back_populates='Utilizador')
    TipoUtilizador_: Mapped['TipoUtilizador'] = relationship('TipoUtilizador', back_populates='Utilizador')
    PedidoManutencao: Mapped[List['PedidoManutencao']] = relationship('PedidoManutencao', back_populates='Utilizador_')
    PedidoNovoRecurso: Mapped[List['PedidoNovoRecurso']] = relationship('PedidoNovoRecurso', back_populates='Utilizador_')
    Recurso: Mapped[List['Recurso']] = relationship('Recurso', back_populates='Utilizador_')
    Voto: Mapped[List['Voto']] = relationship('Voto', back_populates='Utilizador_')
    PedidoReserva: Mapped[List['PedidoReserva']] = relationship('PedidoReserva', back_populates='Utilizador_')


t_NotificacaoUser = Table(
    'NotificacaoUser', Base.metadata,
    Column('NotificacaoID', Integer, primary_key=True, nullable=False),
    Column('UtilizadorID', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['NotificacaoID'], ['Notificacao.NotificacaoID'], name='FKNotificaca868180'),
    ForeignKeyConstraint(['UtilizadorID'], ['Utilizador.UtilizadorID'], name='FKNotificaca496296'),
    PrimaryKeyConstraint('NotificacaoID', 'UtilizadorID', name='PK__Notifica__6294F6408A5AAE8B')
)


class PedidoManutencao(Base):
    __tablename__ = 'PedidoManutencao'
    __table_args__ = (
        ForeignKeyConstraint(['EstadoPedManuID'], ['EstadoPedidoManutencao.EstadoPedManuID'], name='FKPedidoManu183438'),
        ForeignKeyConstraint(['RecComumID'], ['RecursoComun.RecComumID'], name='FKPedidoManu235529'),
        ForeignKeyConstraint(['UtilizadorID'], ['Utilizador.UtilizadorID'], name='FKPedidoManu652837'),
        PrimaryKeyConstraint('PMID', name='PK__PedidoMa__5C86FF66BB44EC2B')
    )

    PMID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    UtilizadorID: Mapped[int] = mapped_column(Integer)
    RecComumID: Mapped[int] = mapped_column(Integer)
    DescPedidoManutencao: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    DataPedido: Mapped[datetime.date] = mapped_column(Date)
    EstadoPedManuID: Mapped[int] = mapped_column(Integer)

    EstadoPedidoManutencao_: Mapped['EstadoPedidoManutencao'] = relationship('EstadoPedidoManutencao', back_populates='PedidoManutencao')
    RecursoComun_: Mapped['RecursoComun'] = relationship('RecursoComun', back_populates='PedidoManutencao')
    Utilizador_: Mapped['Utilizador'] = relationship('Utilizador', back_populates='PedidoManutencao')
    Manutencao: Mapped[List['Manutencao']] = relationship('Manutencao', back_populates='PedidoManutencao_')


class PedidoNovoRecurso(Base):
    __tablename__ = 'PedidoNovoRecurso'
    __table_args__ = (
        ForeignKeyConstraint(['EstadoPedNovoRecID'], ['EstadoPedidoNovoRecurso.EstadoPedNovoRecID'], name='FKPedidoNovo687404'),
        ForeignKeyConstraint(['UtilizadorID'], ['Utilizador.UtilizadorID'], name='FKPedidoNovo924624'),
        PrimaryKeyConstraint('PedidoNovoRecID', name='PK__PedidoNo__0649490BE420AA82')
    )

    PedidoNovoRecID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    UtilizadorID: Mapped[int] = mapped_column(Integer)
    DescPedidoNovoRecurso: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    DataPedido: Mapped[datetime.date] = mapped_column(Date)
    EstadoPedNovoRecID: Mapped[int] = mapped_column(Integer)

    Orcamento_: Mapped[List['Orcamento']] = relationship('Orcamento', secondary='OrcamentoPedidoNovoRecurso', back_populates='PedidoNovoRecurso')
    EstadoPedidoNovoRecurso_: Mapped['EstadoPedidoNovoRecurso'] = relationship('EstadoPedidoNovoRecurso', back_populates='PedidoNovoRecurso')
    Utilizador_: Mapped['Utilizador'] = relationship('Utilizador', back_populates='PedidoNovoRecurso')
    VotacaoPedidoNovoRecurso: Mapped[List['VotacaoPedidoNovoRecurso']] = relationship('VotacaoPedidoNovoRecurso', back_populates='PedidoNovoRecurso_')


class Recurso(Base):
    __tablename__ = 'Recurso'
    __table_args__ = (
        ForeignKeyConstraint(['CatID'], ['Categoria.CatID'], name='FKRecurso936704'),
        ForeignKeyConstraint(['DispID'], ['Disponibilidade.DispID'], name='FKRecurso462257'),
        ForeignKeyConstraint(['UtilizadorID'], ['Utilizador.UtilizadorID'], name='FKRecurso905396'),
        PrimaryKeyConstraint('RecursoID', name='PK__Recurso__82F2B1A4BFA44674')
    )

    RecursoID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Nome: Mapped[str] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DescRecurso: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    Caucao: Mapped[decimal.Decimal] = mapped_column(DECIMAL(19, 0))
    UtilizadorID: Mapped[int] = mapped_column(Integer)
    DispID: Mapped[int] = mapped_column(Integer)
    CatID: Mapped[int] = mapped_column(Integer)
    Imagem: Mapped[Optional[bytes]] = mapped_column(IMAGE)

    Categoria_: Mapped['Categoria'] = relationship('Categoria', back_populates='Recurso')
    Disponibilidade_: Mapped['Disponibilidade'] = relationship('Disponibilidade', back_populates='Recurso')
    Utilizador_: Mapped['Utilizador'] = relationship('Utilizador', back_populates='Recurso')
    PedidoReserva: Mapped[List['PedidoReserva']] = relationship('PedidoReserva', back_populates='Recurso_')


class Voto(Base):
    __tablename__ = 'Voto'
    __table_args__ = (
        ForeignKeyConstraint(['UtilizadorID'], ['Utilizador.UtilizadorID'], name='FKVoto117230'),
        ForeignKeyConstraint(['VotacaoID'], ['Votacao.VotacaoID'], name='FKVoto757754'),
        PrimaryKeyConstraint('VotacaoID', 'UtilizadorID', name='PK__Voto__6DD353A1103635D9')
    )

    VotacaoID: Mapped[int] = mapped_column(Integer, primary_key=True)
    UtilizadorID: Mapped[int] = mapped_column(Integer, primary_key=True)
    EscolhaVoto: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    DataVoto: Mapped[datetime.datetime] = mapped_column(DateTime)

    Utilizador_: Mapped['Utilizador'] = relationship('Utilizador', back_populates='Voto')
    Votacao_: Mapped['Votacao'] = relationship('Votacao', back_populates='Voto')


class Manutencao(Base):
    __tablename__ = 'Manutencao'
    __table_args__ = (
        ForeignKeyConstraint(['EntidadeID'], ['EntidadeExterna.EntidadeID'], name='FKManutencao947029'),
        ForeignKeyConstraint(['EstadoManuID'], ['EstadoManutencao.EstadoManuID'], name='FKManutencao654470'),
        ForeignKeyConstraint(['PMID'], ['PedidoManutencao.PMID'], name='FKManutencao23106'),
        PrimaryKeyConstraint('ManutencaoID', name='PK__Manutenc__8F43BF1225CC3E62')
    )

    ManutencaoID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    PMID: Mapped[int] = mapped_column(Integer)
    EntidadeID: Mapped[int] = mapped_column(Integer)
    DataManutencao: Mapped[datetime.date] = mapped_column(Date)
    DescManutencao: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    EstadoManuID: Mapped[int] = mapped_column(Integer)

    EntidadeExterna_: Mapped['EntidadeExterna'] = relationship('EntidadeExterna', back_populates='Manutencao')
    EstadoManutencao_: Mapped['EstadoManutencao'] = relationship('EstadoManutencao', back_populates='Manutencao')
    PedidoManutencao_: Mapped['PedidoManutencao'] = relationship('PedidoManutencao', back_populates='Manutencao')
    Orcamento_: Mapped[List['Orcamento']] = relationship('Orcamento', secondary='OrcamentoPedidoManutencao', back_populates='Manutencao')
    Votacao_: Mapped[List['Votacao']] = relationship('Votacao', secondary='VotacaoOrcamentoManutencao', back_populates='Manutencao')


t_OrcamentoPedidoNovoRecurso = Table(
    'OrcamentoPedidoNovoRecurso', Base.metadata,
    Column('OrcamentoID', Integer, primary_key=True, nullable=False),
    Column('PedidoNovoRecID', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['OrcamentoID'], ['Orcamento.OrcamentoID'], name='FKOrcamentoP299373'),
    ForeignKeyConstraint(['PedidoNovoRecID'], ['PedidoNovoRecurso.PedidoNovoRecID'], name='FKOrcamentoP11081'),
    PrimaryKeyConstraint('OrcamentoID', 'PedidoNovoRecID', name='PK__Orcament__EEF263C95A8D1045')
)


class PedidoReserva(Base):
    __tablename__ = 'PedidoReserva'
    __table_args__ = (
        ForeignKeyConstraint(['EstadoID'], ['EstadoPedidoReserva.EstadoID'], name='FKPedidoRese354298'),
        ForeignKeyConstraint(['RecursoID'], ['Recurso.RecursoID'], name='FKPedidoRese183537'),
        ForeignKeyConstraint(['UtilizadorID'], ['Utilizador.UtilizadorID'], name='FKPedidoRese738683'),
        PrimaryKeyConstraint('PedidoResevaID', name='PK__PedidoRe__3409FC90E46D3525')
    )

    PedidoResevaID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    UtilizadorID: Mapped[int] = mapped_column(Integer)
    RecursoID: Mapped[int] = mapped_column(Integer)
    DataInicio: Mapped[datetime.date] = mapped_column(Date)
    DataFim: Mapped[datetime.date] = mapped_column(Date)
    EstadoID: Mapped[int] = mapped_column(Integer)

    EstadoPedidoReserva_: Mapped['EstadoPedidoReserva'] = relationship('EstadoPedidoReserva', back_populates='PedidoReserva')
    Recurso_: Mapped['Recurso'] = relationship('Recurso', back_populates='PedidoReserva')
    Utilizador_: Mapped['Utilizador'] = relationship('Utilizador', back_populates='PedidoReserva')
    Reserva: Mapped[List['Reserva']] = relationship('Reserva', back_populates='PedidoReserva_')


class VotacaoPedidoNovoRecurso(Base):
    __tablename__ = 'VotacaoPedidoNovoRecurso'
    __table_args__ = (
        ForeignKeyConstraint(['PedidoNovoRecID'], ['PedidoNovoRecurso.PedidoNovoRecID'], name='FKVotacaoPed723238'),
        ForeignKeyConstraint(['VotacaoID'], ['Votacao.VotacaoID'], name='FKVotacaoPed984472'),
        PrimaryKeyConstraint('TipoVotacao', 'VotacaoID', 'PedidoNovoRecID', name='PK__VotacaoP__6D92E49B54AB4A38')
    )

    TipoVotacao: Mapped[int] = mapped_column(Integer, primary_key=True)
    VotacaoID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PedidoNovoRecID: Mapped[int] = mapped_column(Integer, primary_key=True)

    PedidoNovoRecurso_: Mapped['PedidoNovoRecurso'] = relationship('PedidoNovoRecurso', back_populates='VotacaoPedidoNovoRecurso')
    Votacao_: Mapped['Votacao'] = relationship('Votacao', back_populates='VotacaoPedidoNovoRecurso')


t_OrcamentoPedidoManutencao = Table(
    'OrcamentoPedidoManutencao', Base.metadata,
    Column('OrcamentoID', Integer, primary_key=True, nullable=False),
    Column('ManutencaoID', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['ManutencaoID'], ['Manutencao.ManutencaoID'], name='FKOrcamentoP946778'),
    ForeignKeyConstraint(['OrcamentoID'], ['Orcamento.OrcamentoID'], name='FKOrcamentoP892124'),
    PrimaryKeyConstraint('OrcamentoID', 'ManutencaoID', name='PK__Orcament__7662CCA8ACF39A69')
)


class Reserva(Base):
    __tablename__ = 'Reserva'
    __table_args__ = (
        ForeignKeyConstraint(['PedidoResevaID'], ['PedidoReserva.PedidoResevaID'], name='FKReserva 41673'),
        PrimaryKeyConstraint('ReservaID', name='PK__Reserva__C39937034625B009')
    )

    ReservaID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    PedidoResevaID: Mapped[int] = mapped_column(Integer)
    ConfirmarCaucaoDono: Mapped[bool] = mapped_column(Boolean)
    ConfirmarCaucaoVizinho: Mapped[bool] = mapped_column(Boolean)
    RecursoEntregueDono: Mapped[bool] = mapped_column(Boolean)
    RecursoEntregueVizinho: Mapped[bool] = mapped_column(Boolean)
    DevolucaoCaucao: Mapped[bool] = mapped_column(Boolean)
    EstadoRecurso: Mapped[bool] = mapped_column(Boolean)

    PedidoReserva_: Mapped['PedidoReserva'] = relationship('PedidoReserva', back_populates='Reserva')


t_VotacaoOrcamentoManutencao = Table(
    'VotacaoOrcamentoManutencao', Base.metadata,
    Column('VotacaoID', Integer, primary_key=True, nullable=False),
    Column('ManutencaoID', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['ManutencaoID'], ['Manutencao.ManutencaoID'], name='FKVotacaoOrc476843'),
    ForeignKeyConstraint(['VotacaoID'], ['Votacao.VotacaoID'], name='FKVotacaoOrc131595'),
    PrimaryKeyConstraint('VotacaoID', 'ManutencaoID', name='PK__VotacaoO__CC28E64C9D8E7ADA')
)
