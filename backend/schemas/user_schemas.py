# Requisições ou validação de dados
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    salt: str

class UserResponse(UserBase):
    id: int
    tipo: int

class UserRegistar(BaseModel):
    nome:str
    data_nasc:date
    contacto:int
    email:EmailStr
    password:str
    foto:Optional[str]
    role:str


class Config:
    orm_mode = True