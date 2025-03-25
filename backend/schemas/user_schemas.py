from pydantic import BaseModel, EmailStr
from datetime import date

class User(BaseModel):
    utilizadorID: int
    email: EmailStr
    passwordHash: str
    salt: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegistar(UserLogin):
    nome: str
    data_nasc: date
    contacto: int
    role: str