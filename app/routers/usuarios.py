from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("", response_model=List[schemas.UsuarioResponse], summary="Listar todos los usuarios")
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).options(joinedload(models.Usuario.rol)).all()

@router.get("/{id}", response_model=schemas.UsuarioResponse, summary="Obtener un usuario por ID")
def get_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).options(joinedload(models.Usuario.rol)).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario

@router.post("", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="Crear un usuario")
def create_usuario(user_in: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Usuario).filter(models.Usuario.correo == user_in.correo).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado")
    
    rol = db.query(models.Rol).filter(models.Rol.id == user_in.rol_id).first()
    if not rol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El rol con ID {user_in.rol_id} no existe")

    hashed_pw = auth.hash_password(user_in.password)
    nuevo_usuario = models.Usuario(
        nombre=user_in.nombre,
        correo=user_in.correo,
        password=hashed_pw,
        rol_id=user_in.rol_id
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.put("/{id}", response_model=schemas.UsuarioResponse, summary="Actualizar un usuario")
def update_usuario(id: int, user_in: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    update_data = user_in.model_dump(exclude_unset=True)
    if "correo" in update_data and update_data["correo"] != usuario.correo:
        existing = db.query(models.Usuario).filter(models.Usuario.correo == update_data["correo"]).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está en uso")

    if "password" in update_data and update_data["password"]:
        update_data["password"] = auth.hash_password(update_data["password"])

    if "rol_id" in update_data and update_data["rol_id"]:
        rol = db.query(models.Rol).filter(models.Rol.id == update_data["rol_id"]).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El rol especificado no existe")

    for key, value in update_data.items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/{id}", status_code=status.HTTP_200_OK, summary="Eliminar un usuario")
def delete_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"mensaje": f"Usuario con ID {id} eliminado correctamente"}
