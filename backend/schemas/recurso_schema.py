<<<<<<< HEAD
from enum import Enum

=======
>>>>>>> 7999925 (Atualização de validações e restrições nos dados passados pelos schemas)
from pydantic import BaseModel, constr, conint, condecimal
from typing import Optional
import decimal

# === Schemas Auxiliares ===

class CategoriaSchema(BaseModel):
    CatID: conint(gt=0)
    DescCategoria: constr(min_length=3, max_length=100)

    class Config:
        from_attributes = True

class DisponibilidadeSchema(BaseModel):
    DispID: conint(gt=0)
    DescDisponibilidade: constr(min_length=3, max_length=100)

    class Config:
        from_attributes = True

class UtilizadorSchema(BaseModel):
<<<<<<< HEAD
<<<<<<< HEAD
    UtilizadorID: conint(gt=0)
    NomeUtilizador: constr(min_length=3, max_length=100)
=======
    DispID: conint(gt=0)
    DescDisponibilidade: constr(min_length=3, max_length=100)
>>>>>>> 7999925 (Atualização de validações e restrições nos dados passados pelos schemas)
=======
    UtilizadorID: conint(gt=0)
    NomeUtilizador: constr(min_length=3, max_length=100)
>>>>>>> b429fb6 (Correção de um erro na definição do schema UtilizadorSchema)

    class Config:
        from_attributes = True


# === Inserção de Recurso ===

class RecursoInserirSchema(BaseModel):
    Nome: constr(min_length=2, max_length=100)
    DescRecurso: constr(min_length=5, max_length=500)
    UtilizadorID: conint(gt=0)
    Caucao: condecimal(gt=0, max_digits=10, decimal_places=2)
    CatID: conint(gt=0)
    DispID: conint(gt=0)

    class Config:
        from_attributes = True

# === Recurso para listagens ===

#Informações passadas aquando a amostragem de todos os recurso registados
class RecursoGetTodosSchema(BaseModel):
    RecursoID: conint(gt=0)
    Nome: constr(min_length=2, max_length=100)
    DescRecurso: constr(min_length=5, max_length=500)
    Caucao: condecimal(gt=0, max_digits=10, decimal_places=2)
    Categoria_: CategoriaSchema
    Utilizador_ : UtilizadorSchema
    Disponibilidade_: DisponibilidadeSchema
    Image: Optional[str] = None

    class Config:
        from_attributes = True

#Informação passada aquando da amostragem dos recursos de um utilizador
class RecursoGetUtilizadorSchema(BaseModel):
    RecursoID: conint(gt=0)
    Nome: constr(min_length=2, max_length=100)
    Caucao: condecimal(gt=0, max_digits=10, decimal_places=2)
    Categoria_: CategoriaSchema
    Disponibilidade_: DisponibilidadeSchema

    class Config:
        from_attributes = True

class DisponibilidadeEstadosSchema(str, Enum):
    DISPONIVEL = 1
    INDISPONIVEL = 2