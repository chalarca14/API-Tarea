from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ComentarioBase(BaseModel):
    contenido: str
    tarea_id: int

class ComentarioCreate(ComentarioBase):
    usuario_id: int

class ComentarioUpdate(BaseModel):
    contenido: Optional[str] = None

class ComentarioResponse(BaseModel):
    id: int
    contenido: str
    fecha: datetime
    usuario_id: int
    tarea_id: int
    model_config = ConfigDict(from_attributes=True)

