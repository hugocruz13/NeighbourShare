from pydantic import BaseModel, constr, conint
import datetime
from enum import Enum

class TipoProcessoSchema(BaseModel):
    TipoProcessoID: conint(gt=0)
    DescTipoProcesso: constr(min_length=3, max_length=100)

    class Config:
        from_attributes = True

class NotificacaoUtilizadorSchema(BaseModel):
<<<<<<< HEAD
    UtilizadorID: conint(gt=0)
    NomeUtilizador:  constr(min_length=5, max_length=100)
=======
    NotificacaoID: conint(gt=0)
    UtilizadorID: conint(gt=0)
>>>>>>> 7999925 (Atualização de validações e restrições nos dados passados pelos schemas)

    class Config:
        from_attributes = True

class NotificacaoSchema(BaseModel):
<<<<<<< HEAD
<<<<<<< HEAD
    Titulo: constr(min_length=5, max_length=100)
    Mensagem: constr(min_length=5, max_length=1000)
    ProcessoID: conint(gt=0)
    TipoProcessoID : conint(gt=0)
=======
    Titulo: str
    Mensagem: str
    DataHora: datetime.datetime
    ProcessoID: int
    Estado : bool
    TipoProcID : int
>>>>>>> 9109c73 (Refactor reserva and notificacao services for consistency)
=======
    NotificacaoID: conint(gt=0)
    Mensagem: constr(min_length=5, max_length=500)
    DataHora: datetime.datetime
    ProcessoID: conint(gt=0)
    Estado: conint(ge=0, le=1)
    TipoProcesso_: TipoProcessoSchema
    Utilizador_: NotificacaoUtilizadorSchema
>>>>>>> 7999925 (Atualização de validações e restrições nos dados passados pelos schemas)

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

<<<<<<< HEAD
=======
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

>>>>>>> d732c2c (Add NotificacaoOutSchema and update response model in endpoint)
class TipoProcessoOpcoes(Enum):
    AQUISICAO = "Aquisição"
    MANUTENCAO = "Manutenção"
    RESERVA = "Reserva"
    VOTACAO = "Votação"
