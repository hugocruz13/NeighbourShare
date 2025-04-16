from pydantic import BaseModel, constr, conint, EmailStr

class EntidadeSchema(BaseModel):
    Especialidade: constr(min_length=2, max_length=100)
    Contacto: conint(ge=100000000, le=999999999)
    Email: EmailStr
<<<<<<< HEAD
    Nome: constr(min_length=2, max_length=100)
    Nif: conint(ge=100000000, le=999999999)

class EntidadeUpdateSchema(EntidadeSchema):
    EntidadeID: conint(gt=0)
=======
    Nome: str
    Nif: int

class EntidadeUpdateSchema(BaseModel):
    EntidadeID: int
    Especialidade: str
    Contacto: int
    Email: EmailStr
    Nome: str
    Nif: int
>>>>>>> def1d6c (Add new services, schemas, and endpoints for entity, budget, and resource management)
