from typing import Optional
from pydantic import BaseModel, ConfigDict

class PrioridadBase(BaseModel):
    nombre: str

class PrioridadCreate(PrioridadBase):
    pass

class PrioridadUpdate(BaseModel):
    nombre: Optional[str] = None

class PrioridadResponse(PrioridadBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

