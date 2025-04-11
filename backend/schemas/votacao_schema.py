from pydantic import BaseModel
from datetime import date

class Criar_Votacao(BaseModel):
    titulo: str
    descricao: str
    data_str: date
    data_end: date

class Return_Votacao(Criar_Votacao):
    id:int
