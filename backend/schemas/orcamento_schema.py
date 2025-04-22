<<<<<<< HEAD
<<<<<<< HEAD
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




<<<<<<< HEAD
=======
    class Config:
        from_attributes = True
=======
import decimal
from pydantic import BaseModel
=======
from pydantic import BaseModel, constr, conint, condecimal
>>>>>>> 7999925 (Atualização de validações e restrições nos dados passados pelos schemas)
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
>>>>>>> 101c9b2 (Associação da inserção de um orçamento a um processo em questão, podendo ser ele um pedido de manutenção ou então um pedido de novo recurso comum)

class OrcamentoUpdateSchema(BaseModel):
    OrcamentoID: conint(gt=0)
    Fornecedor: constr(min_length=2, max_length=100)
    Valor: condecimal(gt=0, max_digits=10, decimal_places=2)
    DescOrcamento: constr(min_length=5, max_length=300)

class OrcamentoGetSchema(BaseModel):
<<<<<<< HEAD
    OrcamentoID: int
    Fornecedor: str
    Valor: decimal.Decimal
    DescOrcamento: str
    CaminhoPDF : str
<<<<<<< HEAD
>>>>>>> def1d6c (Add new services, schemas, and endpoints for entity, budget, and resource management)
=======
=======
    OrcamentoID: conint(gt=0)
    Fornecedor: constr(min_length=2, max_length=100)
    Valor: condecimal(gt=0, max_digits=10, decimal_places=2)
    DescOrcamento: constr(min_length=5, max_length=300)
    CaminhoPDF : constr(min_length=5, max_length=300)
>>>>>>> 7999925 (Atualização de validações e restrições nos dados passados pelos schemas)




>>>>>>> 101c9b2 (Associação da inserção de um orçamento a um processo em questão, podendo ser ele um pedido de manutenção ou então um pedido de novo recurso comum)
