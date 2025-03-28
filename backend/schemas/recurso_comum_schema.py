import datetime
from pydantic import BaseModel
from typing import Optional

class UtilizadorSchema(BaseModel):
    UtilizadorID: int
    NomeUtilizador: str

    class Config:
        from_attributes = True

class EstadoPedNovoRecursoSchema(BaseModel):
    EstadoPedNovoRecID: int
    DescEstadoPedidoNovoRecurso: str

    class Config:
        from_attributes = True

class PedidoNovoRecursoSchema(BaseModel):
    PedidoNovoRecID: int
    Utilizador_: UtilizadorSchema
    DescPedidoNovoRecurso: str
    DataPedido: datetime.date
    EstadoPedidoNovoRecurso_: EstadoPedNovoRecursoSchema

    class Config:
        from_attributes = True