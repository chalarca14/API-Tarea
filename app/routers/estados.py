from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/estados", tags=["Estados"])

@router.get("", response_model=List[schemas.EstadoResponse], summary="Listar los estados de las tareas")
def get_estados(db: Session = Depends(get_db)):
    return db.query(models.Estado).all()

@router.get("/{id}", response_model=schemas.EstadoResponse, summary="Obtener un estado por ID")
def get_estado(id: int, db: Session = Depends(get_db)):
    estado = db.query(models.Estado).filter(models.Estado.id == id).first()
    if not estado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estado no encontrado")
    return estado

@router.post("", response_model=schemas.EstadoResponse, status_code=status.HTTP_201_CREATED, summary="Crear un estado")
def create_estado(estado_in: schemas.EstadoCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Estado).filter(models.Estado.nombre == estado_in.nombre).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El estado ya existe")
    nuevo_estado = models.Estado(**estado_in.model_dump())
    db.add(nuevo_estado)
    db.commit()
    db.refresh(nuevo_estado)
    return nuevo_estado

@router.put("/{id}", response_model=schemas.EstadoResponse, summary="Actualizar un estado")
def update_estado(id: int, estado_in: schemas.EstadoUpdate, db: Session = Depends(get_db)):
    estado = db.query(models.Estado).filter(models.Estado.id == id).first()
    if not estado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estado no encontrado")

    update_data = estado_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(estado, key, value)

    db.commit()
    db.refresh(estado)
    return estado

@router.delete("/{id}", status_code=status.HTTP_200_OK, summary="Eliminar un estado")
def delete_estado(id: int, db: Session = Depends(get_db)):
    estado = db.query(models.Estado).filter(models.Estado.id == id).first()
    if not estado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estado no encontrado")

    db.delete(estado)
    db.commit()
    return {"mensaje": f"Estado con ID {id} eliminado correctamente"}

