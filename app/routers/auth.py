from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(tags=["Autenticación"])

@router.post("/register", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo usuario")
def register(user_in: schemas.RegisterRequest, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en la plataforma."""
    existing_user = db.query(models.Usuario).filter(models.Usuario.correo == user_in.correo).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )
    
    rol = db.query(models.Rol).filter(models.Rol.id == user_in.rol_id).first()
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El rol con ID {user_in.rol_id} no existe."
        )

    hashed_pw = auth.hash_password(user_in.password)
    nuevo_usuario = models.Usuario(
        nombre=user_in.nombre,
        correo=user_in.correo,
        password=hashed_pw,
        rol_id=user_in.rol_id,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.post("/login", response_model=schemas.LoginResponse, summary="Iniciar sesión")
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    """Inicia sesión validando credenciales y devuelve un token de acceso."""
    user = db.query(models.Usuario).filter(models.Usuario.correo == credentials.correo).first()
    if not user or not auth.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos."
        )

    token = auth.generate_token()
    return schemas.LoginResponse(
        mensaje="Inicio de sesión exitoso",
        token=token,
        usuario=user
    )

