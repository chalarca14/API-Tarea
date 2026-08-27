import os
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

DATABASE = "taskflow.db"
DB_PATH = BASE_DIR / DATABASE
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH.as_posix()}")

# Configuración del motor SQLAlchemy para SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)

# Activar claves foráneas en SQLite (PRAGMA foreign_keys = ON)
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def obtener_conexion():
    """Retorna una conexión directa de SQLite con claves foráneas activadas y row_factory."""
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def get_db():
    """Generador de sesión SQLAlchemy para FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hashear_password(password: str) -> str:
    """Genera un hash SHA-256 seguro para las contraseñas."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def crear_tablas():
    """Crea todas las tablas del modelo relacional usando cursor.execute() en SQL puro."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # 1. Tabla de roles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    """)

    # 2. Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol_id INTEGER NOT NULL,
            FOREIGN KEY (rol_id) REFERENCES roles(id)
        )
    """)

    # 3. Tabla de proyectos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio DATE,
            fecha_fin DATE
        )
    """)

    # 4. Tabla de categorías
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    """)

    # 5. Tabla de estados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    """)

    # 6. Tabla de prioridades
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prioridades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    """)

    # 7. Tabla de tareas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            proyecto_id INTEGER NOT NULL,
            usuario_id INTEGER,
            categoria_id INTEGER,
            estado_id INTEGER,
            prioridad_id INTEGER,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (categoria_id) REFERENCES categorias(id),
            FOREIGN KEY (estado_id) REFERENCES estados(id),
            FOREIGN KEY (prioridad_id) REFERENCES prioridades(id)
        )
    """)

    # 8. Tabla de comentarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT NOT NULL,
            fecha DATETIME NOT NULL,
            usuario_id INTEGER NOT NULL,
            tarea_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (tarea_id) REFERENCES tareas(id) ON DELETE CASCADE
        )
    """)

    conexion.commit()
    conexion.close()


def sembrar_datos():
    """Siembra los datos iniciales usando cursor.execute() e INSERT OR IGNORE en SQL puro."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # 1. Roles iniciales
    cursor.execute("INSERT OR IGNORE INTO roles (id, nombre) VALUES (1, 'Administrador')")
    cursor.execute("INSERT OR IGNORE INTO roles (id, nombre) VALUES (2, 'Líder de Proyecto')")
    cursor.execute("INSERT OR IGNORE INTO roles (id, nombre) VALUES (3, 'Integrante')")

    # 2. Estados iniciales
    cursor.execute("INSERT OR IGNORE INTO estados (id, nombre) VALUES (1, 'Pendiente')")
    cursor.execute("INSERT OR IGNORE INTO estados (id, nombre) VALUES (2, 'En Progreso')")
    cursor.execute("INSERT OR IGNORE INTO estados (id, nombre) VALUES (3, 'En Revisión')")
    cursor.execute("INSERT OR IGNORE INTO estados (id, nombre) VALUES (4, 'Completada')")

    # 3. Prioridades iniciales
    cursor.execute("INSERT OR IGNORE INTO prioridades (id, nombre) VALUES (1, 'Baja')")
    cursor.execute("INSERT OR IGNORE INTO prioridades (id, nombre) VALUES (2, 'Media')")
    cursor.execute("INSERT OR IGNORE INTO prioridades (id, nombre) VALUES (3, 'Alta')")
    cursor.execute("INSERT OR IGNORE INTO prioridades (id, nombre) VALUES (4, 'Urgente')")

    # 4. Categorías iniciales
    cursor.execute("INSERT OR IGNORE INTO categorias (id, nombre) VALUES (1, 'Desarrollo')")
    cursor.execute("INSERT OR IGNORE INTO categorias (id, nombre) VALUES (2, 'Diseño UI/UX')")
    cursor.execute("INSERT OR IGNORE INTO categorias (id, nombre) VALUES (3, 'Documentación')")
    cursor.execute("INSERT OR IGNORE INTO categorias (id, nombre) VALUES (4, 'Testing')")

    # 5. Usuarios iniciales (con contraseñas hasheadas)
    admin_password = hashear_password("admin123")
    ana_password = hashear_password("ana123")
    narly_password = hashear_password("narly123")

    cursor.execute("""
        INSERT OR IGNORE INTO usuarios (id, nombre, correo, password, rol_id)
        VALUES (?, ?, ?, ?, ?)
    """, (1, "Santiago Sanchez", "admin@taskflow.com", admin_password, 1))

    cursor.execute("""
        INSERT OR IGNORE INTO usuarios (id, nombre, correo, password, rol_id)
        VALUES (?, ?, ?, ?, ?)
    """, (2, "Ana Sofia Rivera", "ana@taskflow.com", ana_password, 2))

    cursor.execute("""
        INSERT OR IGNORE INTO usuarios (id, nombre, correo, password, rol_id)
        VALUES (?, ?, ?, ?, ?)
    """, (3, "Narly Quintero", "narly@taskflow.com", narly_password, 3))

    # 6. Proyecto inicial
    cursor.execute("""
        INSERT OR IGNORE INTO proyectos (id, nombre, descripcion, fecha_inicio, fecha_fin)
        VALUES (1, 'Sistema TaskFlow SENA', 'Desarrollo de la API REST para el sistema de gestión de proyectos y tareas.', '2026-08-01', '2026-11-30')
    """)

    # 7. Tareas iniciales
    cursor.execute("""
        INSERT OR IGNORE INTO tareas (id, titulo, descripcion, proyecto_id, usuario_id, categoria_id, estado_id, prioridad_id)
        VALUES (1, 'Configuración de base de datos SQLite y modelos', 'Diseñar los esquemas relacionales y definir los modelos de base de datos.', 1, 1, 1, 2, 3)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO tareas (id, titulo, descripcion, proyecto_id, usuario_id, categoria_id, estado_id, prioridad_id)
        VALUES (2, 'Documentación de endpoints en OpenAPI/Swagger', 'Completar la guía de aprendizaje y descripción de rutas.', 1, 2, 3, 1, 2)
    """)

    # 8. Comentarios iniciales
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT OR IGNORE INTO comentarios (id, contenido, fecha, usuario_id, tarea_id)
        VALUES (1, 'Se agregaron todas las 8 tablas de la base de datos correctamente con SQL puro.', ?, 1, 1)
    """, (fecha_actual,))

    conexion.commit()
    conexion.close()
