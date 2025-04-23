from pydantic import BaseModel
from datetime import date
from enum import Enum

class TipoVotacao(str, Enum):
    AQUISICAO = "Aquisição"
    MANUTENCAO = "Manutenção"

class Criar_Votacao(BaseModel):
    titulo: str
    descricao: str
    id_processo: int
    data_fim: date
    tipo_votacao: TipoVotacao

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

class Votacao_Return(BaseModel):
    id_votacao: int
    data_inicio: date
    data_fim: date
    processada: bool