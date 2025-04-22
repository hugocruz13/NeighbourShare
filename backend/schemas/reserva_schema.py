import decimal
from enum import Enum
from pydantic import BaseModel
from typing import Optional
import datetime



class UtilizadorSchema(BaseModel):
    UtilizadorID: int
    NomeUtilizador: str
    Contacto: int

    class Config:
        from_attributes = True

class RecursoSchema(BaseModel):
    RecursoID: int
    Nome: str
    DescRecurso: str
    Caucao: decimal.Decimal
    Utilizador_: UtilizadorSchema
    Image: Optional[bytes] = None

    class Config:
        from_attributes = True

class EstadoReservaSchema(BaseModel):
    EstadoID: int
    DescEstadoPedidoReserva: str

    class Config:
        from_attributes = True

class PedidoReservaSchema(BaseModel):
    PedidoResevaID: int
    Utilizador_: UtilizadorSchema
    Recurso_: RecursoSchema
    DataInicio: datetime.date
    DataFim: datetime.date
    EstadoPedidoReserva_: EstadoReservaSchema

class PedidoReservaSchemaCreate(BaseModel):
    UtilizadorID: int
    RecursoID: int
    DataInicio: datetime.date
    DataFim: datetime.date

class PedidoReservaEstadosSchema(Enum):
    EMANALISE = "Em análise"
    APROVADO = "Aprovado"
    REJEITADO = "Rejeitado"

class ReservaSchemaCreate(BaseModel):
    PedidoReservaID: int

class ReservaGetDonoSchema(BaseModel):
    ReservaID: int
    Solicitante: str
    DataInicio: datetime.date
    DataFim: datetime.date
    NomeRecurso: str
    RecursoEntregueDono: bool
    ConfirmarCaucaoDono: bool

class ReservaGetSolicitanteSchema(BaseModel):
    ReservaID: int
    Dono: str
    DataInicio: datetime.date
    DataFim: datetime.date
    NomeRecurso: str
    RecursoEntregueSolicitante: bool
    ConfirmarCaucaoSolicitante: bool
    EstadoReserva: str

class PedidoReservaGetDonoSchema(BaseModel):
    PedidoReservaID: int
    RecursoID: int
    RecursoNome: str
    UtilizadorNome: str
    DataInicio: datetime.date
    DataFim: datetime.date
    EstadoPedidoReserva: str

class PedidoReservaGetSolicitanteSchema(BaseModel):
    PedidoReservaID: int
    RecursoID: int
    RecursoNome: str
    NomeDono: str
    DataInicio: datetime.date
    DataFim: datetime.date
    EstadoPedidoReserva: str


