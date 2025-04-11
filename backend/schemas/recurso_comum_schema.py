import datetime
from pydantic import BaseModel
from typing import Optional

class UtilizadorSchema(BaseModel):
    UtilizadorID: int
    NomeUtilizador: str

    class Config:
        from_attributes = True

class RecursoComunSchema(BaseModel):
    RecComumID: int
    Nome: str
    DescRecursoComum: str
    class Config:
        from_attributes = True

class EstadoPedNovoRecursoSchema(BaseModel):
    EstadoPedNovoRecID: int
    DescEstadoPedidoNovoRecurso: str

    class Config:
        from_attributes = True

class EstadoPedManuSchema(BaseModel):
    EstadoPedManuID: int
    DescEstadoPedidoManutencao: str

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

class PedidoNovoRecursoSchemaCreate(BaseModel):
    UtilizadorID: int
    DescPedidoNovoRecurso: str
    DataPedido: datetime.date

class PedidoManutencaoSchema(BaseModel):
    PMID: int
    Utilizador_: UtilizadorSchema
    RecursoComun_: RecursoComunSchema
    DescPedidoManutencao: str
    DataPedido: datetime.date
    EstadoPedidoManutencao_: EstadoPedManuSchema

    class Config:
        from_attributes = True

class PedidoManutencaoSchemaCreate(BaseModel):
    UtilizadorID: int
    RecursoComumID: int
    DescPedidoManutencao: str
    DataPedido: datetime.date