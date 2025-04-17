from pydantic import BaseModel
import datetime

class TipoProcessoSchema(BaseModel):
    TipoProcessoID: int
    DescTipoProcesso: str

    class Config:
        from_attributes = True

class NotificacaoUtilizadorSchema(BaseModel):
    NotificacaoID: int
    UtilizadorID: int

    class Config:
        from_attributes = True

class NotificacaoSchema(BaseModel):
    NotificacaoID: int
    Mensagem: str
    DataHora: datetime.date
    ProcessoID: int
    Estado: int
    TipoProcesso_: TipoProcessoSchema
    Utilizador_: NotificacaoUtilizadorSchema

    class Config:
        from_attributes = True