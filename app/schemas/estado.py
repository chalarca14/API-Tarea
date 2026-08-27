from typing import Optional
from pydantic import BaseModel, ConfigDict

class EstadoBase(BaseModel):
    nombre: str

class EstadoCreate(EstadoBase):
    pass

class EstadoUpdate(BaseModel):
    nombre: Optional[str] = None

class EstadoResponse(EstadoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

