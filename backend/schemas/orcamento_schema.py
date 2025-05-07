from pydantic import BaseModel, constr, conint, condecimal
from enum import Enum

class TipoOrcamento(str,Enum):
    AQUISICAO = "Aquisição"
    MANUTENCAO = "Manutenção"

class OrcamentoBase(BaseModel):
    IDEntidade: conint(gt=0)
    Valor: condecimal(gt=0, max_digits=10, decimal_places=2)
    DescOrcamento: constr(min_length=5, max_length=300)

class OrcamentoSchema(OrcamentoBase):
    NomePDF : constr(min_length=5, max_length=200)
    IDProcesso: conint(gt=0)
    TipoProcesso: TipoOrcamento

class OrcamentoUpdateSchema(OrcamentoBase):
    OrcamentoID: conint(gt=0)

class OrcamentoGetSchema(OrcamentoBase):
    OrcamentoID: conint(gt=0)
    Entidade: constr(min_length=5, max_length=300)
    CaminhoPDF : constr(min_length=5, max_length=300)




