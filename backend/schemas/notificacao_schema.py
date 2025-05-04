from pydantic import BaseModel, constr, conint
import datetime
from enum import Enum

class TipoProcessoSchema(BaseModel):
    TipoProcessoID: conint(gt=0)
    DescTipoProcesso: constr(min_length=3, max_length=100)

    class Config:
        from_attributes = True

class NotificacaoUtilizadorSchema(BaseModel):
    UtilizadorID: conint(gt=0)
    NomeUtilizador:  constr(min_length=5, max_length=100)

    class Config:
        from_attributes = True

class NotificacaoSchema(BaseModel):
    Titulo: constr(min_length=5, max_length=100)
    Mensagem: constr(min_length=5, max_length=1000)
    ProcessoID: conint(gt=0)
    TipoProcessoID : conint(gt=0)

    class Config:
        from_attributes = True

class NotificacaoOutSchema(BaseModel):
    NotificacaoID: int
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
