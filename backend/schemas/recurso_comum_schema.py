from pydantic import BaseModel, constr, conint
import datetime
from enum import Enum

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
    id:int
    nome: str
    desc:str
    path:str

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

class EstadoPedManutencaoSchema(str,Enum):
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

class PedidoNovoRecursoBase(BaseModel):
    DescPedidoNovoRecurso: constr(min_length=5, max_length=300)
    DataPedido: datetime.date

class PedidoNovoRecursoSchemaCreate(PedidoNovoRecursoBase):
    UtilizadorID: conint(gt=0)
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
<<<<<<< HEAD
    PMID: conint(gt=0)
    DescPedido: constr(min_length=5, max_length=300)
=======
    PMID: int
    DescPedido: str
>>>>>>> dbe2ddb (Ligeira modificação no update de um pedido de manutenção, permitindo somente modificar a descrição do mesmo)

# === Manutenções ===
class ManutencaoBase(BaseModel):
    PMID: conint(gt=0)
    DataManutencao: datetime.date
    DescManutencao: constr(min_length=5, max_length=300)

class ManutencaoInserir(ManutencaoBase):
    EstadoManuID: conint(gt=0)


class ManutencaoSchema(ManutencaoBase):
    ManutencaoID: conint(gt=0)
    EstadoManuID: conint(gt=0)

class ManutencaoCreateSchema(ManutencaoBase):
    Orcamento_id: conint(gt=0)


class ManutencaoUpdateSchema(ManutencaoBase):
    ManutencaoID: conint(gt=0)


# === Atualização de estado ===

class EstadoUpdate(BaseModel):
    novo_estado_id: EstadoPedManutencaoSchema

class PedidoManutencaoRequest(BaseModel):
    recurso_comum_id: int
    desc_manutencao_recurso_comum: str