import decimal
from pydantic import BaseModel
from typing import Optional

class CategoriaSchema(BaseModel):
    CatID: int
    DescCategoria: str

    class Config:
        from_attributes = True

class DisponibilidadeSchema(BaseModel):
    DispID: int
    DescDisponibilidade: str

    class Config:
        from_attributes = True

class UtilizadorSchema(BaseModel):
    UtilizadorID: int
    NomeUtilizador: str

    class Config:
        from_attributes = True

class RecursoSchema(BaseModel):
    Nome: str
    DescRecurso: str
    Caucao: decimal.Decimal
    UtilizadorID: int
    CatID: int
    DispID: int

    class Config:
        from_attributes = True