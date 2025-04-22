from pydantic import BaseModel, constr, conint
import datetime

class TipoProcessoSchema(BaseModel):
    TipoProcessoID: conint(gt=0)
    DescTipoProcesso: constr(min_length=3, max_length=100)

    class Config:
        from_attributes = True

class NotificacaoUtilizadorSchema(BaseModel):
    NotificacaoID: conint(gt=0)
    UtilizadorID: conint(gt=0)

    class Config:
        from_attributes = True

class NotificacaoSchema(BaseModel):
    NotificacaoID: conint(gt=0)
    Mensagem: constr(min_length=5, max_length=500)
    DataHora: datetime.datetime
    ProcessoID: conint(gt=0)
    Estado: conint(ge=0, le=1)
    TipoProcesso_: TipoProcessoSchema
    Utilizador_: NotificacaoUtilizadorSchema

    class Config:
        from_attributes = True