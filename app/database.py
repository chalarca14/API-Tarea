import os
import sqlite3
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
    """Generador de sesión SQLAlchemy para FastAPI (Dependency Injection)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def crear_tablas():
    """Crea todas las tablas del modelo relacional si no existen."""
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)


def sembrar_datos():
    """Siembra los datos iniciales de prueba (roles, estados, prioridades, usuarios, proyectos, etc.)."""
    from app.seed import seed_database
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
