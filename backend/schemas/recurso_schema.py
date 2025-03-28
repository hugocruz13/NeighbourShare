import decimal
from pydantic import BaseModel
from typing import Optional

class CategoriaSchema(BaseModel):
    CatID: int
    Desc: str

    class Config:
        from_attributes = True

class DisponibilidadeSchema(BaseModel):
    DispID: int
    Desc: str

    class Config:
        from_attriutes = True

class UtilizadorSchema(BaseModel):
    UtilizadorID: int
    NomeUtilizador: str

    class Config:
        from_attriutes = True

class RecursoSchema(BaseModel):
    RecursoID: int
    Nome: str
    DescRecurso: str
    Caucao: decimal.Decimal
    Image: Optional[bytes] = None
    utilizador : UtilizadorSchema
    categoria: CategoriaSchema
    disponibilidade: DisponibilidadeSchema

    class Config:
        from_attriutes = True