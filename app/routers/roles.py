from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("", response_model=List[schemas.RolResponse], summary="Listar los roles del sistema")
def get_roles(db: Session = Depends(get_db)):
    return db.query(models.Rol).all()

@router.get("/{id}", response_model=schemas.RolResponse, summary="Obtener un rol por ID")
def get_rol(id: int, db: Session = Depends(get_db)):
    rol = db.query(models.Rol).filter(models.Rol.id == id).first()
    if not rol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    return rol

@router.post("", response_model=schemas.RolResponse, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo rol")
def create_rol(rol_in: schemas.RolCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Rol).filter(models.Rol.nombre == rol_in.nombre).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El rol ya existe")
    nuevo_rol = models.Rol(**rol_in.model_dump())
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return nuevo_rol

@router.put("/{id}", response_model=schemas.RolResponse, summary="Actualizar un rol")
def update_rol(id: int, rol_in: schemas.RolUpdate, db: Session = Depends(get_db)):
    rol = db.query(models.Rol).filter(models.Rol.id == id).first()
    if not rol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    
    update_data = rol_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(rol, key, value)
    
    db.commit()
    db.refresh(rol)
    return rol

@router.delete("/{id}", status_code=status.HTTP_200_OK, summary="Eliminar un rol")
def delete_rol(id: int, db: Session = Depends(get_db)):
    rol = db.query(models.Rol).filter(models.Rol.id == id).first()
    if not rol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    
    if rol.usuarios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el rol porque tiene usuarios asignados."
        )
    
    db.delete(rol)
    db.commit()
    return {"mensaje": f"Rol con ID {id} eliminado correctamente"}

