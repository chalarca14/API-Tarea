import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

# Si no está definida o es relativa, fijarla a la ruta absoluta del proyecto
if not DATABASE_URL or DATABASE_URL == "sqlite:///./taskflow.db":
    db_file_path = BASE_DIR / "taskflow.db"
    DATABASE_URL = f"sqlite:///{db_file_path.as_posix()}"

# SQLite requiere check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
