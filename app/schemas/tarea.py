from typing import Optional
from pydantic import BaseModel, ConfigDict

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

class TareaResponse(TareaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

