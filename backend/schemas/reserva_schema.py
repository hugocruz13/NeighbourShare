import decimal

from pydantic import BaseModel
from typing import Optional
import datetime

class RecursoSchema(BaseModel):
    RecursoID: int
    Nome: str
    DescRecurso: str
    Caucao: decimal.Decimal
    Image: Optional[bytes] = None

    class Config:
        from_attributes = True

class UtilizadorSchema(BaseModel):
    UtilizadorID: int
    NomeUtilizador: str

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

class ReservaSchemaCreate(BaseModel):
    PedidoReservaID: int

