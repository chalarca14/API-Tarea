from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("", response_model=List[schemas.CategoriaResponse], summary="Listar las categorías")
def get_categorias(db: Session = Depends(get_db)):
    return db.query(models.Categoria).all()

@router.get("/{id}", response_model=schemas.CategoriaResponse, summary="Obtener una categoría por ID")
def get_categoria(id: int, db: Session = Depends(get_db)):
    cat = db.query(models.Categoria).filter(models.Categoria.id == id).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return cat

@router.post("", response_model=schemas.CategoriaResponse, status_code=status.HTTP_201_CREATED, summary="Crear una categoría")
def create_categoria(cat_in: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Categoria).filter(models.Categoria.nombre == cat_in.nombre).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La categoría ya existe")
    nueva_cat = models.Categoria(**cat_in.model_dump())
    db.add(nueva_cat)
    db.commit()
    db.refresh(nueva_cat)
    return nueva_cat

@router.put("/{id}", response_model=schemas.CategoriaResponse, summary="Actualizar una categoría")
def update_categoria(id: int, cat_in: schemas.CategoriaUpdate, db: Session = Depends(get_db)):
    cat = db.query(models.Categoria).filter(models.Categoria.id == id).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")

    update_data = cat_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cat, key, value)

    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/{id}", status_code=status.HTTP_200_OK, summary="Eliminar una categoría")
def delete_categoria(id: int, db: Session = Depends(get_db)):
    cat = db.query(models.Categoria).filter(models.Categoria.id == id).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")

    db.delete(cat)
    db.commit()
    return {"mensaje": f"Categoría con ID {id} eliminada correctamente"}

