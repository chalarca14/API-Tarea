from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ProyectoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class ProyectoResponse(ProyectoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

