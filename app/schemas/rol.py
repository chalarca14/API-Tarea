from typing import Optional
from pydantic import BaseModel, ConfigDict

class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: Optional[str] = None

class RolResponse(RolBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

