from pydantic import BaseModel, EmailStr, validator
from datetime import date
from utils.PasswordHasher import validate_password_strength

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
    @validator('password')
    def validate_password(cls, value):
        return validate_password_strength(value)

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    password: str
    @validator('password')
    def validate_password(cls, value):
        return validate_password_strength(value)