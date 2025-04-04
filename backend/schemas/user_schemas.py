from pydantic import BaseModel, EmailStr
from datetime import date

class User(BaseModel):
    utilizador_ID: int
    email: EmailStr
    password_hash: str
    salt: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegistar(BaseModel):
    email: EmailStr
    role: str

class UserJWT(BaseModel):
    id: int
    email: EmailStr
    role: str

class NewUserUpdate(BaseModel):
    nome: str
    data_nascimento: date
    contacto: int
    password: str

class AuthResult\
            (BaseModel):
    token: str
    role: str