import decimal
from pydantic import BaseModel
from typing import Optional
from fastapi import File

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

class RecursoInserirSchema(BaseModel):
    Nome: str
    DescRecurso: str
    UtilizadorID: int
    Caucao: decimal.Decimal
    CatID: int
    DispID: int
    Image: Optional[bytes] = None

    class Config:
        from_attributes = True

#Informações passadas aquando a amostragem de todos os recurso registados
class RecursoGetTodosSchema(BaseModel):
    RecursoID: int
    Nome: str
    DescRecurso: str
    Caucao: decimal.Decimal
    Categoria_: CategoriaSchema
    Disponibilidade_: DisponibilidadeSchema
    Image: Optional[str] = None

    class Config:
        from_attributes = True

#Informação passada aquando da amostragem dos recursos de um utilizador
class RecursoGetUtilizadorSchema(BaseModel):
    RecursoID: int
    Nome: str
    Caucao: decimal.Decimal
    Categoria_: CategoriaSchema
    Disponibilidade_: DisponibilidadeSchema

    class Config:
        from_attributes = True