from pydantic import BaseModel, constr, conint, EmailStr

class EntidadeSchema(BaseModel):
    Especialidade: constr(min_length=2, max_length=100)
    Contacto: conint(ge=100000000, le=999999999)
    Email: EmailStr
    Nome: constr(min_length=2, max_length=100)
    Nif: conint(ge=100000000, le=999999999)

class EntidadeUpdateSchema(BaseModel):
    EntidadeID: conint(gt=0)
    Especialidade: constr(min_length=2, max_length=100)
    Contacto: conint(ge=100000000, le=999999999)
    Email: EmailStr
    Nome: constr(min_length=2, max_length=100)
    Nif: conint(ge=100000000, le=999999999)