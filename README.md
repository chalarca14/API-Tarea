# 📋 TaskFlow API - SENA

API RESTful para la gestión de proyectos, tareas y equipos de trabajo colaborativo, desarrollada con **FastAPI**, **SQLAlchemy** y base de datos **SQLite**.

---

## 🏗️ Estructura del Proyecto

```text
Api tarea/
├── app/
│   ├── models/           # Modelos de SQLAlchemy separados por entidad
│   │   ├── __init__.py
│   │   ├── rol.py
│   │   ├── usuario.py
│   │   ├── proyecto.py
│   │   ├── categoria.py
│   │   ├── estado.py
│   │   ├── prioridad.py
│   │   ├── tarea.py
│   │   └── comentario.py
│   ├── routers/          # Rutas y endpoints modulares
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── roles.py
│   │   ├── usuarios.py
│   │   ├── proyectos.py
│   │   ├── categorias.py
│   │   ├── estados.py
│   │   ├── prioridades.py
│   │   ├── tareas.py
│   │   └── comentarios.py
│   ├── schemas/          # Esquemas Pydantic v2 separados por entidad
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── rol.py
│   │   ├── usuario.py
│   │   ├── proyecto.py
│   │   ├── categoria.py
│   │   ├── estado.py
│   │   ├── prioridad.py
│   │   ├── tarea.py
│   │   └── comentario.py
│   ├── __init__.py
│   ├── auth.py           # Utilidades de hashing y autenticación
│   ├── database.py       # Configuración de base de datos SQLite y sesión
│   ├── main.py           # Aplicación principal FastAPI y configuración CORS
│   └── seed.py           # Poblamiento automático con datos de prueba
├── .env                  # Variables de entorno
├── requirements.txt      # Dependencias del proyecto
├── taskflow.db           # Base de datos SQLite (visualizable con SQLite Viewer)
└── README.md
```

---

## ⚙️ Instalación y Puesta en Marcha

1. **Activar el entorno virtual:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Instalar dependencias (si aplica):**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Iniciar el servidor:**
   ```powershell
   uvicorn app.main:app --reload
   ```

4. **Acceder a la Documentación Interactiva:**
   * **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   * **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🗄️ Visualización de Base de Datos con SQLite Viewer

1. Instala la extensión **SQLite Viewer** en VS Code.
2. Haz clic sobre el archivo `taskflow.db` en el explorador de archivos para consultar tablas y registros.

---

## 👥 Usuarios de Prueba Registrados

* **Administrador:** `admin@taskflow.com` | `admin123`
* **Líder de Proyecto:** `ana@taskflow.com` | `ana123`
* **Integrante:** `narly@taskflow.com` | `narly123`

