from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    estado_id = Column(Integer, ForeignKey("estados.id"), nullable=True)
    prioridad_id = Column(Integer, ForeignKey("prioridades.id"), nullable=True)

    proyecto = relationship("Proyecto", back_populates="tareas")
    usuario = relationship("Usuario", back_populates="tareas")
    categoria = relationship("Categoria", back_populates="tareas")
    estado = relationship("Estado", back_populates="tareas")
    prioridad = relationship("Prioridad", back_populates="tareas")
    comentarios = relationship("Comentario", back_populates="tarea", cascade="all, delete-orphan")

