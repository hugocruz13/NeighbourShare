from pydantic import BaseModel
import datetime
from enum import Enum

class TipoProcessoSchema(BaseModel):
    TipoProcessoID: int
    DescTipoProcesso: str

    class Config:
        from_attributes = True

class NotificacaoUtilizadorSchema(BaseModel):
    UtilizadorID: int
    NomeUtilizador: str

    class Config:
        from_attributes = True

class NotificacaoSchema(BaseModel):
    Titulo: str
    Mensagem: str
    DataHora: datetime.datetime
    ProcessoID: int
    Estado : bool
    TipoProcID : int

    class Config:
        from_attributes = True

class TipoProcessoOpcoes(Enum):
    AQUISICAO = "Aquisição"
    MANUTENCAO = "Manutenção"
    RESERVA = "Reserva"
    VOTACAO = "Votação"
