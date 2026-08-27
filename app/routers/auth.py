from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
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
async def login(request: Request, db: Session = Depends(get_db)):
    """
    Inicia sesión validando credenciales y devuelve un token JWT firmado.
    Soporta tanto JSON (`{"correo": "...", "password": "..."}`) como Form Data de OAuth2 (para el botón 'Authorize' de Swagger).
    """
    content_type = request.headers.get("content-type", "").lower()
    correo = None
    password = None

    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form = await request.form()
        correo = form.get("username") or form.get("correo")
        password = form.get("password")
    else:
        try:
            body = await request.json()
            correo = body.get("correo") or body.get("username")
            password = body.get("password")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de solicitud no válido. Debe enviar JSON o Form Data."
            )

    if not correo or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debe proporcionar correo/username y password."
        )

    user = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if not user or not auth.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos."
        )

    jwt_token = auth.create_access_token(
        data={
            "sub": user.correo,
            "user_id": user.id,
            "rol": user.rol.nombre if user.rol else "Integrante"
        }
    )
    
    return schemas.LoginResponse(
        mensaje="Inicio de sesión exitoso",
        access_token=jwt_token,
        token_type="bearer",
        usuario=user
    )


@router.get("/me", response_model=schemas.UsuarioResponse, summary="Obtener perfil del usuario autenticado (Protegido con JWT)")
def get_current_user_profile(current_user: models.Usuario = Depends(auth.get_current_user)):
    """Devuelve la información del usuario autenticado a partir del token JWT Bearer."""
    return current_user
