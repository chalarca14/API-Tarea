from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/prioridades", tags=["Prioridades"])

@router.get("", response_model=List[schemas.PrioridadResponse], summary="Listar las prioridades")
def get_prioridades(db: Session = Depends(get_db)):
    return db.query(models.Prioridad).all()

@router.get("/{id}", response_model=schemas.PrioridadResponse, summary="Obtener una prioridad por ID")
def get_prioridad(id: int, db: Session = Depends(get_db)):
    prioridad = db.query(models.Prioridad).filter(models.Prioridad.id == id).first()
    if not prioridad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prioridad no encontrada")
    return prioridad

@router.post("", response_model=schemas.PrioridadResponse, status_code=status.HTTP_201_CREATED, summary="Crear una prioridad")
def create_prioridad(prio_in: schemas.PrioridadCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Prioridad).filter(models.Prioridad.nombre == prio_in.nombre).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La prioridad ya existe")
    nueva_prio = models.Prioridad(**prio_in.model_dump())
    db.add(nueva_prio)
    db.commit()
    db.refresh(nueva_prio)
    return nueva_prio

@router.put("/{id}", response_model=schemas.PrioridadResponse, summary="Actualizar una prioridad")
def update_prioridad(id: int, prio_in: schemas.PrioridadUpdate, db: Session = Depends(get_db)):
    prioridad = db.query(models.Prioridad).filter(models.Prioridad.id == id).first()
    if not prioridad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prioridad no encontrada")

    update_data = prio_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(prioridad, key, value)

    db.commit()
    db.refresh(prioridad)
    return prioridad

@router.delete("/{id}", status_code=status.HTTP_200_OK, summary="Eliminar una prioridad")
def delete_prioridad(id: int, db: Session = Depends(get_db)):
    prioridad = db.query(models.Prioridad).filter(models.Prioridad.id == id).first()
    if not prioridad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prioridad no encontrada")

    db.delete(prioridad)
    db.commit()
    return {"mensaje": f"Prioridad con ID {id} eliminada correctamente"}

