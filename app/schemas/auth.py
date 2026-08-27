from typing import Optional
from pydantic import BaseModel, EmailStr
from app.schemas.usuario import UsuarioResponse

class RegisterRequest(BaseModel):
    nombre: str
    correo: EmailStr
    password: str
    rol_id: Optional[int] = 3  # Por defecto 'Integrante'

class LoginRequest(BaseModel):
    correo: EmailStr
    password: str

class LoginResponse(BaseModel):
    mensaje: str
    token: str
    usuario: UsuarioResponse

