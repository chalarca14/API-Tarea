from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, field_validator

class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    proyecto_id: int
    usuario_id: Optional[int] = None
    categoria_id: Optional[int] = None
    estado_id: Optional[int] = None
    prioridad_id: Optional[int] = None

class TareaCreate(TareaBase):
    pass

class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    proyecto_id: Optional[int] = None
    usuario_id: Optional[int] = None
    categoria_id: Optional[int] = None
    estado_id: Optional[int] = None
    prioridad_id: Optional[int] = None

class TareaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str] = None
    proyecto: Optional[str] = None
    usuario: Optional[str] = None
    categoria: Optional[str] = None
    estado: Optional[str] = None
    prioridad: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("proyecto", mode="before")
    @classmethod
    def extract_proyecto(cls, v: Any) -> Optional[str]:
        if hasattr(v, "nombre"):
            return v.nombre
        elif isinstance(v, dict) and "nombre" in v:
            return v["nombre"]
        return str(v) if v is not None else None

    @field_validator("usuario", mode="before")
    @classmethod
    def extract_usuario(cls, v: Any) -> Optional[str]:
        if hasattr(v, "nombre"):
            return v.nombre
        elif isinstance(v, dict) and "nombre" in v:
            return v["nombre"]
        return str(v) if v is not None else None

    @field_validator("categoria", mode="before")
    @classmethod
    def extract_categoria(cls, v: Any) -> Optional[str]:
        if hasattr(v, "nombre"):
            return v.nombre
        elif isinstance(v, dict) and "nombre" in v:
            return v["nombre"]
        return str(v) if v is not None else None

    @field_validator("estado", mode="before")
    @classmethod
    def extract_estado(cls, v: Any) -> Optional[str]:
        if hasattr(v, "nombre"):
            return v.nombre
        elif isinstance(v, dict) and "nombre" in v:
            return v["nombre"]
        return str(v) if v is not None else None

    @field_validator("prioridad", mode="before")
    @classmethod
    def extract_prioridad(cls, v: Any) -> Optional[str]:
        if hasattr(v, "nombre"):
            return v.nombre
        elif isinstance(v, dict) and "nombre" in v:
            return v["nombre"]
        return str(v) if v is not None else None
