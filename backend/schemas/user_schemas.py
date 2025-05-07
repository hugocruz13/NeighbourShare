from pydantic import BaseModel, EmailStr, validator,conint, constr, Field
from typing import Optional
from datetime import date
from utils.PasswordHasher import validate_password_strength

class User(BaseModel):
    utilizador_ID: conint(gt=0)
    email: EmailStr
    password_hash: str
    salt: str
    role: constr(min_length=3, max_length=20)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegistar(BaseModel):
    email: EmailStr
    role: constr(min_length=3, max_length=20)

    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ['admin', 'residente', 'gestor']  # Exemplo de papéis válidos
        if v not in allowed_roles:
            raise ValueError(f"Role deve ser um dos: {', '.join(allowed_roles)}")
        return v

class UserJWT(BaseModel):
    id: conint(gt=0)
    email: EmailStr
    role: str

class UserData(BaseModel):
    nome: constr(min_length=3, max_length=100)
    email: EmailStr
    contacto: conint(ge=100000000, le=999999999)
    data_nascimento: date
    imagem: str

class NewUserUpdate(BaseModel):
    nome: constr(min_length=3, max_length=100)
    data_nascimento: date
    contacto: conint(ge=100000000, le=999999999)
    password: str
    path :Optional[str] = Field(default=None, example= "")
    @validator('password')
    def validate_password(cls, value):
        return validate_password_strength(value)

class UserUpdateInfo(BaseModel):
    nome: Optional[str] = Field(default=None, example= "")
    contacto: Optional[int]
    data_nascimento: Optional[date]

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    password: str
    @validator('password')
    def validate_password(cls, value):
        return validate_password_strength(value)