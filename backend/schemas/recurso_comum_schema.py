from pydantic import BaseModel, constr, conint, ConfigDict
import datetime
from enum import Enum
from typing import Optional


# === Utilizadores e Recursos Comuns ===

class UtilizadorSchema(BaseModel):
    UtilizadorID: conint(gt=0)
    NomeUtilizador: constr(min_length=3, max_length=100)

    class Config:
        from_attributes = True

class RecursoComunSchema(BaseModel):
    RecComumID: conint(gt=0)
    Nome: constr(min_length=2, max_length=100)
    DescRecursoComum: constr(min_length=5, max_length=300)

    class Config:
        from_attributes = True

class RecursoComumSchemaCreate(BaseModel):
    Nome: constr(min_length=2, max_length=100)
    DescRecursoComum: constr(min_length=5, max_length=300)

    class Config:
        from_attributes = True

class RecursoComum_Return(BaseModel):
    id: conint(gt=0)
    nome: constr(min_length=2, max_length=100)
    desc: constr(min_length=5, max_length=300)
    path: constr(min_length=5, max_length=300)

class RecursoComunUpdate(BaseModel):
    Nome: Optional[str] = None
    DescRecursoComum: Optional[str] = None
    Path: Optional[str] = None


# === Estados ===

class EstadoPedNovoRecursoSchema(BaseModel):
    EstadoPedNovoRecID: conint(gt=0)
    DescEstadoPedidoNovoRecurso: constr(min_length=3, max_length=100)

    class Config:
        from_attributes = True

class EstadoPedManuSchema(BaseModel):
    EstadoPedManuID: conint(gt=0)
    DescEstadoPedidoManutencao: constr(min_length=3, max_length=100)

    class Config:
        from_attributes = True

class EstadoPedNovoRecursoComumSchema(str,Enum):
    PENDENTE = 'Pendente'
    EMVOTACAO = 'Em votação'
    REJEITADO = 'Rejeitado'
    APROVADOPARAORCAMENTACAO = 'Aprovado para orçamentação'
    REJEITADOAPOSORCAMENTACAO = 'Rejeitado após orçamentação'
    APROVADOPARACOMPRA = 'Aprovado para compra'
    CONCLUIDO = 'Concluído'

class EstadoPedManutencaoSchema(int,Enum):
    EMANALISE = 1
    APROVADOEXECUCAOINTERNA = 2
    NEGOCIACAOENTIDADESEXTERNAS = 3
    VOTACAO = 5
    REJEITADO = 4


# === Pedidos de Novo Recurso ===

class PedidoNovoRecursoSchema(BaseModel):
    PedidoNovoRecID: conint(gt=0)
    Utilizador_: UtilizadorSchema
    DescPedidoNovoRecurso: constr(min_length=5, max_length=300)
    DataPedido: datetime.date
    EstadoPedidoNovoRecurso_: EstadoPedNovoRecursoSchema

    class Config:
        from_attributes = True

class PedidoNovoRecursoSchemaCreate(BaseModel):
    UtilizadorID: conint(gt=0)
    DescPedidoNovoRecurso: constr(min_length=5, max_length=300)
    DataPedido: datetime.date
    EstadoPedNovoRecID: conint(gt=0)


# === Pedidos de Manutenção ===

class PedidoManutencaoSchema(BaseModel):
    PMID: conint(gt=0)
    Utilizador_: UtilizadorSchema
    RecursoComun_: RecursoComunSchema
    DescPedido: constr(min_length=5, max_length=300)
    DataPedido: datetime.date
    EstadoPedidoManutencao_: EstadoPedManuSchema

    class Config:
        from_attributes = True

class PedidoManutencaoSchemaCreate(BaseModel):
    UtilizadorID: conint(gt=0)
    RecComumID: conint(gt=0)
    DescPedido: constr(min_length=5, max_length=300)
    DataPedido: datetime.date
    EstadoPedManuID: conint(gt=0)

class PedidoManutencaoUpdateSchema(BaseModel):
    PMID: conint(gt=0)
    DescPedido: constr(min_length=5, max_length=300)

# === Manutenções ===
class ManutencaoInserir(BaseModel):
    PMID: conint(gt=0)
    DataManutencao: datetime.date
    DescManutencao: constr(min_length=5, max_length=300)
    EstadoManuID: conint(gt=0)


class ManutencaoSchema(BaseModel):
    ManutencaoID: conint(gt=0)
    PMID: conint(gt=0)
    DataManutencao: datetime.date
    DescManutencao: constr(min_length=5, max_length=300)
    EstadoManuID: conint(gt=0)

class ManutencaoCreateSchema(BaseModel):
    PMID: conint(gt=0)
    DataManutencao: datetime.date
    DescManutencao: constr(min_length=5, max_length=300)
    Orcamento_id: conint(gt=0)


class ManutencaoUpdateSchema(BaseModel):
    ManutencaoID: conint(gt=0)
    PMID: conint(gt=0)
    DataManutencao: datetime.date
    DescManutencao: constr(min_length=5, max_length=300)

# === Atualização de estado ===

class EstadoUpdate(BaseModel):
    novo_estado_id: EstadoPedManutencaoSchema

class PedidoManutencaoRequest(BaseModel):
    recurso_comum_id: int
    desc_manutencao_recurso_comum: str