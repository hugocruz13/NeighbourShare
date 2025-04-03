import decimal
from pydantic import BaseModel

class OrcamentoSchema(BaseModel):
    Fornecedor: str
    Valor: decimal.Decimal
    DescOrcamento: str
    NomePDF : str

    class Config:
        from_attributes = True