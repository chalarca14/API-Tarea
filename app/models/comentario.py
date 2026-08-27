from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Comentario(Base):
    __tablename__ = "comentarios"

    id = Column(Integer, primary_key=True, index=True)
    contenido = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tarea_id = Column(Integer, ForeignKey("tareas.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="comentarios")
    tarea = relationship("Tarea", back_populates="comentarios")

