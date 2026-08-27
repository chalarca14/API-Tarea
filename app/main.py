from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import joinedload
from app.database import engine, Base, SessionLocal, crear_tablas, sembrar_datos
from app import models
from app.routers import (
    auth,
    roles,
    usuarios,
    proyectos,
    categorias,
    estados,
    prioridades,
    tareas,
    comentarios,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas en SQLite y sembrar datos iniciales
    crear_tablas()
    sembrar_datos()
    yield

app = FastAPI(
    title="TaskFlow API - SENA",
    description="""
    API RESTful para la gestión integral de proyectos, tareas, equipos y comentarios.
    
    **Entidades soportadas:**
    * **Roles**: Administrador, Líder de Proyecto, Integrante.
    * **Usuarios**: Gestión de miembros del equipo y credenciales.
    * **Proyectos**: Control de proyectos y fechas de entrega.
    * **Tareas**: Asignación, categorías, estados y niveles de prioridad.
    * **Comentarios**: Interacción y seguimiento colaborativo.
    * **Categorías, Estados y Prioridades**: Clasificación paramétrica.
    """,
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Equipo TaskFlow (SENA)",
        "email": "contacto@taskflow.sena.edu.co"
    }
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers
app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(categorias.router)
app.include_router(estados.router)
app.include_router(prioridades.router)
app.include_router(tareas.router)
app.include_router(comentarios.router)

@app.get("/", tags=["General"], summary="Ruta de bienvenida y estado de la API")
def root():
    return {
        "sistema": "TaskFlow API",
        "estado": "Activo y funcionando",
        "base_de_datos": "SQLite (taskflow.db)",
        "visor_visual_db": "/dashboard",
        "documentacion_swagger": "/docs",
        "documentacion_redoc": "/redoc"
    }

@app.get("/dashboard", response_class=HTMLResponse, tags=["General"], summary="Visor visual de la Base de Datos")
def database_dashboard():
    """Genera un visor web interactivo en tiempo real de todas las tablas de SQLite."""
    db = SessionLocal()
    try:
        roles_data = db.query(models.Rol).all()
        usuarios_data = db.query(models.Usuario).options(joinedload(models.Usuario.rol)).all()
        proyectos_data = db.query(models.Proyecto).all()
        categorias_data = db.query(models.Categoria).all()
        estados_data = db.query(models.Estado).all()
        prioridades_data = db.query(models.Prioridad).all()
        tareas_data = db.query(models.Tarea).options(
            joinedload(models.Tarea.proyecto),
            joinedload(models.Tarea.usuario),
            joinedload(models.Tarea.categoria),
            joinedload(models.Tarea.estado),
            joinedload(models.Tarea.prioridad),
        ).all()
        comentarios_data = db.query(models.Comentario).options(
            joinedload(models.Comentario.usuario),
            joinedload(models.Comentario.tarea)
        ).all()

        usuarios_rows = "".join(
            f"<tr><td><span class='badge bg-dark'>{u.id}</span></td><td class='fw-semibold'>{u.nombre}</td><td><code>{u.correo}</code></td><td class='text-muted small'>{u.password[:20]}...</td><td><span class='badge bg-info text-dark'>{u.rol.nombre if u.rol else u.rol_id}</span></td></tr>"
            for u in usuarios_data
        )

        tareas_rows = "".join(
            f"<tr><td><span class='badge bg-dark'>{t.id}</span></td><td class='fw-bold'>{t.titulo}</td><td class='text-muted small'>{t.descripcion or 'N/A'}</td><td>{t.proyecto.nombre if t.proyecto else t.proyecto_id}</td><td>{t.usuario.nombre if t.usuario else 'Sin asignar'}</td><td><span class='badge bg-secondary'>{t.categoria.nombre if t.categoria else 'N/A'}</span></td><td><span class='badge bg-warning text-dark'>{t.estado.nombre if t.estado else 'N/A'}</span></td><td><span class='badge bg-danger'>{t.prioridad.nombre if t.prioridad else 'N/A'}</span></td></tr>"
            for t in tareas_data
        )

        proyectos_rows = "".join(
            f"<tr><td><span class='badge bg-dark'>{p.id}</span></td><td class='fw-bold'>{p.nombre}</td><td>{p.descripcion}</td><td><code>{p.fecha_inicio}</code></td><td><code>{p.fecha_fin}</code></td></tr>"
            for p in proyectos_data
        )

        comentarios_rows = "".join(
            f"<tr><td><span class='badge bg-dark'>{c.id}</span></td><td>{c.contenido}</td><td><code>{c.fecha.strftime('%Y-%m-%d %H:%M')}</code></td><td>{c.usuario.nombre if c.usuario else c.usuario_id}</td><td>#{c.tarea_id} - {c.tarea.titulo if c.tarea else ''}</td></tr>"
            for c in comentarios_data
        )

        roles_rows = "".join(
            f"<tr><td><span class='badge bg-dark'>{r.id}</span></td><td class='fw-semibold'>{r.nombre}</td></tr>"
            for r in roles_data
        )

        categorias_rows = "".join(
            f"<tr><td><span class='badge bg-dark'>{cat.id}</span></td><td class='fw-semibold'>{cat.nombre}</td></tr>"
            for cat in categorias_data
        )

        estados_rows = "".join(
            f"<tr><td><span class='badge bg-dark'>{e.id}</span></td><td class='fw-semibold'>{e.nombre}</td></tr>"
            for e in estados_data
        )

        prioridades_rows = "".join(
            f"<tr><td><span class='badge bg-dark'>{pr.id}</span></td><td class='fw-semibold'>{pr.nombre}</td></tr>"
            for pr in prioridades_data
        )
    finally:
        db.close()

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TaskFlow DB Viewer - SENA</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
        <style>
            body {{ background-color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; }}
            .card {{ border-radius: 12px; border: none; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05); }}
            .nav-pills .nav-link.active {{ background-color: #0284c7; }}
            .nav-pills .nav-link {{ color: #475569; font-weight: 500; }}
        </style>
    </head>
    <body class="p-4">
        <div class="container-fluid">
            <div class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom">
                <div>
                    <h2 class="fw-bold text-dark m-0"><i class="bi bi-database text-primary me-2"></i>TaskFlow - Visor de Base de Datos SQLite</h2>
                    <p class="text-muted m-0">Archivo: <code>taskflow.db</code> | Estado: <span class="badge bg-success">Conectado y Actualizado</span></p>
                </div>
                <div>
                    <a href="/docs" target="_blank" class="btn btn-outline-primary me-2"><i class="bi bi-journal-code me-1"></i>Swagger Docs</a>
                    <button onclick="location.reload()" class="btn btn-primary"><i class="bi bi-arrow-clockwise me-1"></i>Refrescar Datos</button>
                </div>
            </div>

            <!-- Navegación por pestañas de las 8 tablas -->
            <ul class="nav nav-pills mb-4 gap-2" id="dbTabs" role="tablist">
                <li class="nav-item">
                    <button class="nav-link active" data-bs-toggle="pill" data-bs-target="#tab-usuarios" type="button">
                        <i class="bi bi-people me-1"></i>Usuarios <span class="badge bg-secondary ms-1">{len(usuarios_data)}</span>
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="pill" data-bs-target="#tab-tareas" type="button">
                        <i class="bi bi-check2-square me-1"></i>Tareas <span class="badge bg-secondary ms-1">{len(tareas_data)}</span>
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="pill" data-bs-target="#tab-proyectos" type="button">
                        <i class="bi bi-kanban me-1"></i>Proyectos <span class="badge bg-secondary ms-1">{len(proyectos_data)}</span>
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="pill" data-bs-target="#tab-comentarios" type="button">
                        <i class="bi bi-chat-dots me-1"></i>Comentarios <span class="badge bg-secondary ms-1">{len(comentarios_data)}</span>
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="pill" data-bs-target="#tab-roles" type="button">
                        <i class="bi bi-shield-lock me-1"></i>Roles <span class="badge bg-secondary ms-1">{len(roles_data)}</span>
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="pill" data-bs-target="#tab-categorias" type="button">
                        <i class="bi bi-tag me-1"></i>Categorías <span class="badge bg-secondary ms-1">{len(categorias_data)}</span>
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="pill" data-bs-target="#tab-estados" type="button">
                        <i class="bi bi-toggle-on me-1"></i>Estados <span class="badge bg-secondary ms-1">{len(estados_data)}</span>
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="pill" data-bs-target="#tab-prioridades" type="button">
                        <i class="bi bi-flag me-1"></i>Prioridades <span class="badge bg-secondary ms-1">{len(prioridades_data)}</span>
                    </button>
                </li>
            </ul>

            <!-- Contenido de las pestañas -->
            <div class="tab-content">
                <!-- USUARIOS -->
                <div class="tab-pane fade show active" id="tab-usuarios">
                    <div class="card p-3">
                        <h5 class="fw-bold mb-3"><i class="bi bi-people text-primary me-2"></i>Tabla: <code>usuarios</code></h5>
                        <div class="table-responsive">
                            <table class="table table-hover align-middle">
                                <thead class="table-light">
                                    <tr>
                                        <th>ID</th>
                                        <th>Nombre</th>
                                        <th>Correo</th>
                                        <th>Password (Hash SHA-256)</th>
                                        <th>Rol</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {usuarios_rows}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- TAREAS -->
                <div class="tab-pane fade" id="tab-tareas">
                    <div class="card p-3">
                        <h5 class="fw-bold mb-3"><i class="bi bi-check2-square text-primary me-2"></i>Tabla: <code>tareas</code></h5>
                        <div class="table-responsive">
                            <table class="table table-hover align-middle">
                                <thead class="table-light">
                                    <tr>
                                        <th>ID</th>
                                        <th>Título</th>
                                        <th>Descripción</th>
                                        <th>Proyecto</th>
                                        <th>Responsable</th>
                                        <th>Categoría</th>
                                        <th>Estado</th>
                                        <th>Prioridad</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {tareas_rows}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- PROYECTOS -->
                <div class="tab-pane fade" id="tab-proyectos">
                    <div class="card p-3">
                        <h5 class="fw-bold mb-3"><i class="bi bi-kanban text-primary me-2"></i>Tabla: <code>proyectos</code></h5>
                        <div class="table-responsive">
                            <table class="table table-hover align-middle">
                                <thead class="table-light">
                                    <tr>
                                        <th>ID</th>
                                        <th>Nombre</th>
                                        <th>Descripción</th>
                                        <th>Fecha Inicio</th>
                                        <th>Fecha Fin</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {proyectos_rows}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- COMENTARIOS -->
                <div class="tab-pane fade" id="tab-comentarios">
                    <div class="card p-3">
                        <h5 class="fw-bold mb-3"><i class="bi bi-chat-dots text-primary me-2"></i>Tabla: <code>comentarios</code></h5>
                        <div class="table-responsive">
                            <table class="table table-hover align-middle">
                                <thead class="table-light">
                                    <tr>
                                        <th>ID</th>
                                        <th>Contenido</th>
                                        <th>Fecha</th>
                                        <th>Usuario</th>
                                        <th>Tarea</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {comentarios_rows}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- ROLES -->
                <div class="tab-pane fade" id="tab-roles">
                    <div class="card p-3">
                        <h5 class="fw-bold mb-3"><i class="bi bi-shield-lock text-primary me-2"></i>Tabla: <code>roles</code></h5>
                        <table class="table table-hover">
                            <thead class="table-light"><tr><th>ID</th><th>Nombre del Rol</th></tr></thead>
                            <tbody>
                                {roles_rows}
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- CATEGORIAS -->
                <div class="tab-pane fade" id="tab-categorias">
                    <div class="card p-3">
                        <h5 class="fw-bold mb-3"><i class="bi bi-tag text-primary me-2"></i>Tabla: <code>categorias</code></h5>
                        <table class="table table-hover">
                            <thead class="table-light"><tr><th>ID</th><th>Nombre de Categoría</th></tr></thead>
                            <tbody>
                                {categorias_rows}
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- ESTADOS -->
                <div class="tab-pane fade" id="tab-estados">
                    <div class="card p-3">
                        <h5 class="fw-bold mb-3"><i class="bi bi-toggle-on text-primary me-2"></i>Tabla: <code>estados</code></h5>
                        <table class="table table-hover">
                            <thead class="table-light"><tr><th>ID</th><th>Nombre de Estado</th></tr></thead>
                            <tbody>
                                {estados_rows}
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- PRIORIDADES -->
                <div class="tab-pane fade" id="tab-prioridades">
                    <div class="card p-3">
                        <h5 class="fw-bold mb-3"><i class="bi bi-flag text-primary me-2"></i>Tabla: <code>prioridades</code></h5>
                        <table class="table table-hover">
                            <thead class="table-light"><tr><th>ID</th><th>Nombre de Prioridad</th></tr></thead>
                            <tbody>
                                {prioridades_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return html
