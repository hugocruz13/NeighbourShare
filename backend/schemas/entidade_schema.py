from pydantic import BaseModel, EmailStr


class EntidadeSchema(BaseModel):
    Especialidade: str
    Contacto: int
    Email: EmailStr
    Nome: str
    Nif: int