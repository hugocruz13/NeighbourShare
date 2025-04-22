from pydantic import BaseModel, constr, conint, condecimal
from enum import Enum

class TipoOrcamento(str,Enum):
    AQUISICAO = "Aquisição"
    MANUTENCAO = "Manutenção"

class OrcamentoSchema(BaseModel):
    Fornecedor: constr(min_length=2, max_length=100)
    Valor: condecimal(gt=0, max_digits=10, decimal_places=2)
    DescOrcamento: constr(min_length=5, max_length=300)
    NomePDF : constr(min_length=5, max_length=200)
    IDProcesso: conint(gt=0)
    TipoProcesso: TipoOrcamento

class OrcamentoUpdateSchema(BaseModel):
    OrcamentoID: conint(gt=0)
    Fornecedor: constr(min_length=2, max_length=100)
    Valor: condecimal(gt=0, max_digits=10, decimal_places=2)
    DescOrcamento: constr(min_length=5, max_length=300)

class OrcamentoGetSchema(BaseModel):
    OrcamentoID: conint(gt=0)
    Fornecedor: constr(min_length=2, max_length=100)
    Valor: condecimal(gt=0, max_digits=10, decimal_places=2)
    DescOrcamento: constr(min_length=5, max_length=300)
    CaminhoPDF : constr(min_length=5, max_length=300)




