<<<<<<< HEAD
from pydantic import BaseModel, constr, conint, EmailStr
=======
from pydantic import BaseModel, EmailStr, constr, conint

>>>>>>> 7999925 (Atualização de validações e restrições nos dados passados pelos schemas)

class EntidadeSchema(BaseModel):
    Especialidade: constr(min_length=2, max_length=100)
    Contacto: conint(ge=100000000, le=999999999)
    Email: EmailStr
<<<<<<< HEAD
<<<<<<< HEAD
    Nome: constr(min_length=2, max_length=100)
    Nif: conint(ge=100000000, le=999999999)

class EntidadeUpdateSchema(EntidadeSchema):
    EntidadeID: conint(gt=0)
=======
    Nome: str
    Nif: int
=======
    Nome: constr(min_length=2, max_length=100)
    Nif: conint(ge=100000000, le=999999999)
>>>>>>> 7999925 (Atualização de validações e restrições nos dados passados pelos schemas)

class EntidadeUpdateSchema(BaseModel):
    EntidadeID: conint(gt=0)
    Especialidade: constr(min_length=2, max_length=100)
    Contacto: conint(ge=100000000, le=999999999)
    Email: EmailStr
<<<<<<< HEAD
    Nome: str
    Nif: int
>>>>>>> def1d6c (Add new services, schemas, and endpoints for entity, budget, and resource management)
=======
    Nome: constr(min_length=2, max_length=100)
    Nif: conint(ge=100000000, le=999999999)
>>>>>>> 7999925 (Atualização de validações e restrições nos dados passados pelos schemas)
