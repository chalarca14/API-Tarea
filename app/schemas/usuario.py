from typing import Optional, Any
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol_id: int

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None
    rol_id: Optional[int] = None

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("rol", mode="before")
    @classmethod
    def extract_rol_nombre(cls, v: Any) -> str:
        if hasattr(v, "nombre"):
            return v.nombre
        elif isinstance(v, dict) and "nombre" in v:
            return v["nombre"]
        return str(v)
