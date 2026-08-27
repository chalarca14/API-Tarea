from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])

@router.get("", response_model=List[schemas.ComentarioResponse], summary="Listar los comentarios (Protegido)")
def get_comentarios(
    tarea_id: Optional[int] = Query(None, description="Filtrar comentarios por tarea"),
    usuario_id: Optional[int] = Query(None, description="Filtrar comentarios por usuario"),
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    query = db.query(models.Comentario)
    if tarea_id:
        query = query.filter(models.Comentario.tarea_id == tarea_id)
    if usuario_id:
        query = query.filter(models.Comentario.usuario_id == usuario_id)
    return query.all()

@router.get("/{id}", response_model=schemas.ComentarioResponse, summary="Obtener un comentario por ID (Protegido)")
def get_comentario(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    comentario = db.query(models.Comentario).filter(models.Comentario.id == id).first()
    if not comentario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")
    return comentario

@router.post("", response_model=schemas.ComentarioResponse, status_code=status.HTTP_201_CREATED, summary="Crear un comentario (Protegido)")
def create_comentario(
    comentario_in: schemas.ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == comentario_in.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario especificado no existe")

    tarea = db.query(models.Tarea).filter(models.Tarea.id == comentario_in.tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La tarea especificada no existe")

    nuevo_comentario = models.Comentario(**comentario_in.model_dump())
    db.add(nuevo_comentario)
    db.commit()
    db.refresh(nuevo_comentario)
    return nuevo_comentario

@router.put("/{id}", response_model=schemas.ComentarioResponse, summary="Actualizar un comentario (Protegido)")
def update_comentario(
    id: int,
    comentario_in: schemas.ComentarioUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    comentario = db.query(models.Comentario).filter(models.Comentario.id == id).first()
    if not comentario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")

    # Solo el autor o un Administrador puede editar el comentario
    rol_actual = current_user.rol.nombre if current_user.rol else ""
    if comentario.usuario_id != current_user.id and rol_actual != "Administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes editar un comentario que no fue creado por ti."
        )

    update_data = comentario_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(comentario, key, value)

    db.commit()
    db.refresh(comentario)
    return comentario

@router.delete("/{id}", status_code=status.HTTP_200_OK, summary="Eliminar un comentario (Protegido)")
def delete_comentario(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    comentario = db.query(models.Comentario).filter(models.Comentario.id == id).first()
    if not comentario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")

    # Solo el autor o un Administrador puede eliminar el comentario
    rol_actual = current_user.rol.nombre if current_user.rol else ""
    if comentario.usuario_id != current_user.id and rol_actual != "Administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes eliminar un comentario que no fue creado por ti."
        )

    db.delete(comentario)
    db.commit()
    return {"mensaje": f"Comentario con ID {id} eliminado correctamente"}
