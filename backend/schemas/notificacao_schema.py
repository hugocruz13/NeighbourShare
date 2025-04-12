from pydantic import BaseModel
import datetime

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
    DataHora: datetime.date
    ProcessoID: int
    TipoProcessoID : int
    UtilizadorID: int

    class Config:
        from_attributes = True