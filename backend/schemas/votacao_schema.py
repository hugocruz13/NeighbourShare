from pydantic import BaseModel
from datetime import date

class Criar_Votacao_Novo_Recurso(BaseModel):
    titulo: str
    descricao: str
    data_fim: date
    id_pedido:int

class Criar_Votacao_Manutenção(BaseModel):
    titulo: str
    descricao: str
    data_fim: date
    id_manutencao:int

class Votar(BaseModel):
    voto:str
    id_votacao:int

class Votar_id(BaseModel):
    voto:str
    id_votacao:int
    id_user:int

class Consulta_Votacao(BaseModel):
    id_votacao: int
    id_user: int