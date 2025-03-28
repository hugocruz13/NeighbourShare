import decimal

from pydantic import BaseModel
from datetime import datetime

class RecursoSchema(BaseModel):
    RecursoID: int
    Nome: str
    DescRecurso: str
    Caucao: decimal.Decimal
    Image: bytes
    DisponibilidadeID: int
    CategoriaID: int

    class Config:
        orm_mode = True