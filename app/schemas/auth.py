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
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse

    # Propiedad de compatibilidad
    @property
    def token(self) -> str:
        return self.access_token
