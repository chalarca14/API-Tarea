from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Prioridad(Base):
    __tablename__ = "prioridades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    tareas = relationship("Tarea", back_populates="prioridad")

