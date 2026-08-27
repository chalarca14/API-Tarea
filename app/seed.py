from datetime import date, datetime
from sqlalchemy.orm import Session
from app import models, auth

def seed_database(db: Session):
    """Inserta datos iniciales de prueba si la base de datos está vacía."""
    # 1. Roles
    if db.query(models.Rol).count() == 0:
        roles = [
            models.Rol(id=1, nombre="Administrador"),
            models.Rol(id=2, nombre="Líder de Proyecto"),
            models.Rol(id=3, nombre="Integrante"),
        ]
        db.add_all(roles)
        db.commit()

    # 2. Estados
    if db.query(models.Estado).count() == 0:
        estados = [
            models.Estado(id=1, nombre="Pendiente"),
            models.Estado(id=2, nombre="En Progreso"),
            models.Estado(id=3, nombre="En Revisión"),
            models.Estado(id=4, nombre="Completada"),
        ]
        db.add_all(estados)
        db.commit()

    # 3. Prioridades
    if db.query(models.Prioridad).count() == 0:
        prioridades = [
            models.Prioridad(id=1, nombre="Baja"),
            models.Prioridad(id=2, nombre="Media"),
            models.Prioridad(id=3, nombre="Alta"),
            models.Prioridad(id=4, nombre="Urgente"),
        ]
        db.add_all(prioridades)
        db.commit()

    # 4. Categorías
    if db.query(models.Categoria).count() == 0:
        categorias = [
            models.Categoria(id=1, nombre="Desarrollo"),
            models.Categoria(id=2, nombre="Diseño UI/UX"),
            models.Categoria(id=3, nombre="Documentación"),
            models.Categoria(id=4, nombre="Testing"),
        ]
        db.add_all(categorias)
        db.commit()

    # 5. Usuarios iniciales
    if db.query(models.Usuario).count() == 0:
        admin_user = models.Usuario(
            id=1,
            nombre="Santiago Sanchez",
            correo="admin@taskflow.com",
            password=auth.hash_password("admin123"),
            rol_id=1,
        )
        lider_user = models.Usuario(
            id=2,
            nombre="Ana Sofia Rivera",
            correo="ana@taskflow.com",
            password=auth.hash_password("ana123"),
            rol_id=2,
        )
        integrante_user = models.Usuario(
            id=3,
            nombre="Narly Quintero",
            correo="narly@taskflow.com",
            password=auth.hash_password("narly123"),
            rol_id=3,
        )
        db.add_all([admin_user, lider_user, integrante_user])
        db.commit()

    # 6. Proyecto inicial
    if db.query(models.Proyecto).count() == 0:
        proyecto1 = models.Proyecto(
            id=1,
            nombre="Sistema TaskFlow SENA",
            descripcion="Desarrollo de la API REST para el sistema de gestión de proyectos y tareas.",
            fecha_inicio=date(2026, 8, 1),
            fecha_fin=date(2026, 11, 30),
        )
        db.add(proyecto1)
        db.commit()

    # 7. Tareas iniciales
    if db.query(models.Tarea).count() == 0:
        tarea1 = models.Tarea(
            id=1,
            titulo="Configuración de base de datos SQLite y modelos",
            descripcion="Diseñar los esquemas relacionales y definir los modelos de SQLAlchemy.",
            proyecto_id=1,
            usuario_id=1,
            categoria_id=1,
            estado_id=2,
            prioridad_id=3,
        )
        tarea2 = models.Tarea(
            id=2,
            titulo="Documentación de endpoints en OpenAPI/Swagger",
            descripcion="Completar la guía de aprendizaje y descripción de rutas.",
            proyecto_id=1,
            usuario_id=2,
            categoria_id=3,
            estado_id=1,
            prioridad_id=2,
        )
        db.add_all([tarea1, tarea2])
        db.commit()

    # 8. Comentario inicial
    if db.query(models.Comentario).count() == 0:
        comentario1 = models.Comentario(
            id=1,
            contenido="Se agregaron todas las 8 tablas de la base de datos correctamente.",
            fecha=datetime.now(),
            usuario_id=1,
            tarea_id=1,
        )
        db.add(comentario1)
        db.commit()

