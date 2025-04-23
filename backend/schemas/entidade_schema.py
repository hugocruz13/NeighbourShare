from pydantic import BaseModel, EmailStr

class EntidadeSchema(BaseModel):
    Especialidade: str
    Contacto: int
    Email: EmailStr
    Nome: str
    Nif: int

class EntidadeUpdateSchema(BaseModel):
    EntidadeID: int
    Especialidade: str
    Contacto: int
    Email: EmailStr
    Nome: str
    Nif: int