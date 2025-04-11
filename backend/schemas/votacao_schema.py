from pydantic import BaseModel
from datetime import date

class Criar_Votacao(BaseModel):
    titulo: str
    descricao: str
    data_str: date
    data_end: date

class Return_Votacao(Criar_Votacao):
    id:int

class Pedido_Novo_Recurso(BaseModel):
    id_votacao:int
    id_pedido:int