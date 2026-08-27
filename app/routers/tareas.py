from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/tareas", tags=["Tareas"])

@router.get("", response_model=List[schemas.TareaResponse], summary="Listar todas las tareas")
def get_tareas(
    proyecto_id: Optional[int] = Query(None, description="Filtrar tareas por proyecto"),
    usuario_id: Optional[int] = Query(None, description="Filtrar tareas por usuario"),
    estado_id: Optional[int] = Query(None, description="Filtrar tareas por estado"),
    prioridad_id: Optional[int] = Query(None, description="Filtrar tareas por prioridad"),
    categoria_id: Optional[int] = Query(None, description="Filtrar tareas por categoría"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Tarea)
    if proyecto_id:
        query = query.filter(models.Tarea.proyecto_id == proyecto_id)
    if usuario_id:
        query = query.filter(models.Tarea.usuario_id == usuario_id)
    if estado_id:
        query = query.filter(models.Tarea.estado_id == estado_id)
    if prioridad_id:
        query = query.filter(models.Tarea.prioridad_id == prioridad_id)
    if categoria_id:
        query = query.filter(models.Tarea.categoria_id == categoria_id)
    return query.all()

@router.get("/{id}", response_model=schemas.TareaResponse, summary="Obtener una tarea por ID")
def get_tarea(id: int, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == id).first()
    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return tarea

@router.post("", response_model=schemas.TareaResponse, status_code=status.HTTP_201_CREATED, summary="Crear una nueva tarea")
def create_tarea(tarea_in: schemas.TareaCreate, db: Session = Depends(get_db)):
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == tarea_in.proyecto_id).first()
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto especificado no existe")

    if tarea_in.usuario_id:
        if not db.query(models.Usuario).filter(models.Usuario.id == tarea_in.usuario_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario especificado no existe")

    if tarea_in.categoria_id:
        if not db.query(models.Categoria).filter(models.Categoria.id == tarea_in.categoria_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La categoría especificada no existe")

    if tarea_in.estado_id:
        if not db.query(models.Estado).filter(models.Estado.id == tarea_in.estado_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El estado especificado no existe")

    if tarea_in.prioridad_id:
        if not db.query(models.Prioridad).filter(models.Prioridad.id == tarea_in.prioridad_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La prioridad especificada no existe")

    nueva_tarea = models.Tarea(**tarea_in.model_dump())
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea

@router.put("/{id}", response_model=schemas.TareaResponse, summary="Actualizar una tarea")
def update_tarea(id: int, tarea_in: schemas.TareaUpdate, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == id).first()
    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    update_data = tarea_in.model_dump(exclude_unset=True)

    if "proyecto_id" in update_data and update_data["proyecto_id"]:
        if not db.query(models.Proyecto).filter(models.Proyecto.id == update_data["proyecto_id"]).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto especificado no existe")

    if "usuario_id" in update_data and update_data["usuario_id"]:
        if not db.query(models.Usuario).filter(models.Usuario.id == update_data["usuario_id"]).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario especificado no existe")

    if "categoria_id" in update_data and update_data["categoria_id"]:
        if not db.query(models.Categoria).filter(models.Categoria.id == update_data["categoria_id"]).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La categoría especificada no existe")

    if "estado_id" in update_data and update_data["estado_id"]:
        if not db.query(models.Estado).filter(models.Estado.id == update_data["estado_id"]).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El estado especificado no existe")

    if "prioridad_id" in update_data and update_data["prioridad_id"]:
        if not db.query(models.Prioridad).filter(models.Prioridad.id == update_data["prioridad_id"]).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La prioridad especificada no existe")

    for key, value in update_data.items():
        setattr(tarea, key, value)

    db.commit()
    db.refresh(tarea)
    return tarea

@router.delete("/{id}", status_code=status.HTTP_200_OK, summary="Eliminar una tarea")
def delete_tarea(id: int, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == id).first()
    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    db.delete(tarea)
    db.commit()
    return {"mensaje": f"Tarea con ID {id} eliminada correctamente"}

