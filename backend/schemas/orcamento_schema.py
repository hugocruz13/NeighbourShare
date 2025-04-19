import decimal
from pydantic import BaseModel
from enum import Enum

class TipoOrcamento(Enum):
    AQUISICAO = "Aquisição"
    MANUTENCAO = "Manutenção"

class OrcamentoSchema(BaseModel):
    Fornecedor: str
    Valor: decimal.Decimal
    DescOrcamento: str
    NomePDF : str
    IDProcesso: int
    TipoProcesso: TipoOrcamento

class OrcamentoUpdateSchema(BaseModel):
    OrcamentoID: int
    Fornecedor: str
    Valor: decimal.Decimal
    DescOrcamento: str

class OrcamentoGetSchema(BaseModel):
    OrcamentoID: int
    Fornecedor: str
    Valor: decimal.Decimal
    DescOrcamento: str
    CaminhoPDF : str




