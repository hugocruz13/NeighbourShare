from pydantic import BaseModel, constr, conint, condecimal, validator
from typing import Optional
import decimal
import datetime
from enum import Enum


# === Recursos, Utilizadores e Estado ===



class UtilizadorSchema(BaseModel):
    UtilizadorID: conint(gt=0)
    NomeUtilizador: constr(min_length=3, max_length=100)
    Contacto: conint(ge=100000000, le=999999999)

    class Config:
        from_attributes = True

class RecursoSchema(BaseModel):
    RecursoID: conint(gt=0)
    Nome: constr(min_length=2, max_length=100)
    DescRecurso: constr(min_length=5, max_length=500)
    Caucao: condecimal(gt=0, max_digits=10, decimal_places=2)
    Utilizador_: UtilizadorSchema
    Image: Optional[bytes] = None

    class Config:
        from_attributes = True

class EstadoReservaSchema(BaseModel):
    EstadoID: conint(gt=0)
    DescEstadoPedidoReserva: constr(min_length=3, max_length=100)

    class Config:
        from_attributes = True

# === Pedido de Reserva ===

class PedidoReservaSchema(BaseModel):
    PedidoResevaID: conint(gt=0)
    Utilizador_: UtilizadorSchema
    Recurso_: RecursoSchema
    DataInicio: datetime.date
    DataFim: datetime.date
    EstadoPedidoReserva_: EstadoReservaSchema

    @validator('DataInicio', 'DataFim')
    def data_nao_pode_ser_no_passado(cls, v):
        if v < datetime.date.today():
            raise ValueError('A data não pode ser anterior ao dia atual')
        return v

    @validator('DataFim')
    def fim_deve_ser_maior_que_inicio(cls, v, values):
        if 'DataInicio' in values and v < values['DataInicio']:
            raise ValueError('DataFim deve ser posterior ou igual a DataInicio')
        return v

class PedidoReservaSchemaCreate(BaseModel):
    UtilizadorID: conint(gt=0)
    RecursoID: conint(gt=0)
    DataInicio: datetime.date
    DataFim: datetime.date

    @validator('DataInicio', 'DataFim')
    def data_nao_pode_ser_no_passado(cls, v):
        if v < datetime.date.today():
            raise ValueError('A data não pode ser anterior ao dia atual')
        return v

    @validator('DataFim')
    def fim_deve_ser_maior_que_inicio(cls, v, values):
        if 'DataInicio' in values and v < values['DataInicio']:
            raise ValueError('DataFim deve ser posterior ou igual a DataInicio')
        return v

class PedidoReservaEstadosSchema(str, Enum):
    EMANALISE = "Em análise"
    APROVADO = "Aprovado"
    REJEITADO = "Rejeitado"

class ReservaSchemaCreate(BaseModel):
    PedidoReservaID: conint(gt=0)

class ReservaGetDonoSchema(BaseModel):
    ReservaID: conint(gt=0)
    Solicitante: constr(min_length=3, max_length=100)
    DataInicio: datetime.date
    DataFim: datetime.date
    NomeRecurso: constr(min_length=2, max_length=100)
    RecursoEntregueDono: bool
    ConfirmarCaucaoDono: bool
    DevolucaoCaucao: bool
    EstadoRecurso: bool
    JustificacaoEstadoProduto : constr(min_length=2, max_length=500)

class ReservaGetSolicitanteSchema(BaseModel):
    ReservaID: conint(gt=0)
    Dono: constr(min_length=3, max_length=100)
    DataInicio: datetime.date
    DataFim: datetime.date
    NomeRecurso: constr(min_length=2, max_length=100)
    RecursoEntregueSolicitante: bool
    ConfirmarCaucaoSolicitante: bool
    EstadoReserva: constr(min_length=3, max_length=100)

# === Listagem de Pedidos de Reserva ===

class PedidoReservaGetDonoSchema(BaseModel):
    PedidoReservaID: conint(gt=0)
    RecursoID: conint(gt=0)
    RecursoNome: constr(min_length=2, max_length=100)
    UtilizadorNome: constr(min_length=3, max_length=100)
    DataInicio: datetime.date
    DataFim: datetime.date
    EstadoPedidoReserva: constr(min_length=3, max_length=100)

class PedidoReservaGetSolicitanteSchema(BaseModel):
    PedidoReservaID: conint(gt=0)
    RecursoID: conint(gt=0)
    RecursoNome: constr(min_length=2, max_length=100)
    NomeDono: constr(min_length=3, max_length=100)
    DataInicio: datetime.date
    DataFim: datetime.date
    EstadoPedidoReserva: constr(min_length=3, max_length=100)


