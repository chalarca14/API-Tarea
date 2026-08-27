from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.get("", response_model=List[schemas.ProyectoResponse], summary="Listar todos los proyectos")
def get_proyectos(db: Session = Depends(get_db)):
    return db.query(models.Proyecto).all()

@router.get("/{id}", response_model=schemas.ProyectoResponse, summary="Obtener un proyecto por ID")
def get_proyecto(id: int, db: Session = Depends(get_db)):
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == id).first()
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    return proyecto

@router.post("", response_model=schemas.ProyectoResponse, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo proyecto")
def create_proyecto(proy_in: schemas.ProyectoCreate, db: Session = Depends(get_db)):
    nuevo_proyecto = models.Proyecto(**proy_in.model_dump())
    db.add(nuevo_proyecto)
    db.commit()
    db.refresh(nuevo_proyecto)
    return nuevo_proyecto

@router.put("/{id}", response_model=schemas.ProyectoResponse, summary="Actualizar un proyecto")
def update_proyecto(id: int, proy_in: schemas.ProyectoUpdate, db: Session = Depends(get_db)):
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == id).first()
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")

    update_data = proy_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(proyecto, key, value)

    db.commit()
    db.refresh(proyecto)
    return proyecto

@router.delete("/{id}", status_code=status.HTTP_200_OK, summary="Eliminar un proyecto")
def delete_proyecto(id: int, db: Session = Depends(get_db)):
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == id).first()
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")

    db.delete(proyecto)
    db.commit()
    return {"mensaje": f"Proyecto con ID {id} eliminado correctamente"}

