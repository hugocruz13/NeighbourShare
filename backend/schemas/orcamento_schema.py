import decimal
from pydantic import BaseModel

class OrcamentoSchema(BaseModel):
    Fornecedor: str
    Valor: decimal.Decimal
    DescOrcamento: str
    NomePDF : str

    class Config:
        from_attributes = True

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