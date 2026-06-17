# FlamejBresto — Plataforma de Gestión y Reservas

Aplicación web para el restaurante **FlamejBresto**, desarrollada como proyecto final de la materia. El sistema permite a los clientes realizar reservas, consultar el menú y dejar reseñas, y provee al personal un panel de administración centralizado con dashboards analíticos.

## Arquitectura

```
  Browser (cliente)
       |
       v
  Flask Frontend  (puerto 5000)
       |
       | HTTP / requests
       v
  Flask Backend API  (puerto 5001)
       |
       v
  MySQL
```

El sistema se compone de **dos aplicaciones Flask independientes**:

- **Frontend** (`frontend/`): sirve los templates Jinja2 al navegador. No accede directamente a la base de datos; consume la API del backend mediante la librería `requests`.
- **Backend** (`backend/`): API REST pura. Gestiona la lógica de negocio, accede a MySQL y envía emails automáticos con Flask-Mail.

## Estructura del proyecto

```
proyecto_final/
├── setup_entorno_virtual.sh        # Script de instalación y setup completo
├── backend/
│   ├── app.py                      # Entry point del backend (puerto 5001)
│   ├── requirements.txt
│   ├── .env.example
│   ├── crear_admin.py              # Script para crear el usuario administrador inicial
│   ├── pagination.py               # Utilidad de paginación HATEOAS
│   ├── utils.py
│   ├── database/
│   │   └── database.sql            # Script SQL de creación de tablas
│   └── routes/                     # Blueprints de la API
│       ├── auth.py                 # POST /auth/login
│       ├── menu.py                 # CRUD /platos
│       ├── reservas.py             # CRUD /reservas + QR + emails
│       ├── reseñas.py              # CRUD /reseñas + gráficos
│       ├── servicios_extra.py      # CRUD /restaurante/servicios-extra
│       └── panel_control_dashboard.py  # GET /dashboard/*
└── frontend/
    ├── app.py                      # Entry point del frontend (puerto 5000)
    ├── config.py                   # Configuración (API_BASE_URL, SECRET_KEY)
    ├── requirements.txt
    ├── .env.example
    ├── routes/                     # Blueprints del frontend
    │   ├── inicio.py               # GET /
    │   ├── auth.py                 # GET|POST /login
    │   ├── admin.py                # GET /admin
    │   ├── menu.py                 # CRUD /admin/menu
    │   ├── reservas.py             # POST /reservas + CRUD /admin/reservas
    │   ├── reseñas.py              # CRUD /admin/resenas + formulario cliente
    │   ├── scanner.py              # GET|POST /admin/scanner
    │   └── servicios_extra.py      # CRUD /admin/servicios
    ├── templates/                  # Vistas Jinja2
    └── static/
        ├── css/
        ├── scripts/
        └── Imagenes/
```

## Requisitos previos

- Python 3.10+
- MySQL corriendo localmente
- Cuenta de Gmail con **contraseña de aplicación** habilitada (para el envío de emails)

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd proyecto_final
```

### 2. Configurar los archivos `.env`

Antes de correr el setup, creá los archivos `.env` en ambas carpetas a partir de los ejemplos provistos:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Completá las variables en cada archivo (ver sección [Variables de entorno](#variables-de-entorno)).

### 3. Correr el script de setup

```bash
chmod +x setup_entorno_virtual.sh
./setup_entorno_virtual.sh
```

El script realiza automáticamente los siguientes pasos:
1. Solicita la contraseña de root de MySQL
2. Crea la base de datos y todas las tablas ejecutando `backend/database/database.sql`
3. Crea un entorno virtual Python (`venv/`)
4. Instala las dependencias del backend (`backend/requirements.txt`)
5. Instala las dependencias del frontend (`frontend/requirements.txt`)
6. Ejecuta `backend/crear_admin.py` para crear el usuario administrador inicial

### 4. Levantar ambos servidores

Una vez finalizado el setup, levantá cada app en una terminal separada:

**Terminal 1 — Backend:**
```bash
source venv/bin/activate
cd backend
flask run --port 5001 o python3 app.py
```

**Terminal 2 — Frontend:**
```bash
source venv/bin/activate
cd frontend
flask run --port 5000 o python3 app.py
```

La aplicación estará disponible en `http://localhost:5000/`.

## Variables de entorno

Ambos `.env` son independientes. A continuación se describen las variables de cada uno.

### `backend/.env`

| Variable              | Descripción                                        | Ejemplo                  |
|-----------------------|----------------------------------------------------|--------------------------|
| `DB_HOST`             | Host de MySQL                                      |  `localhost`             |
| `DB_USER`             | Usuario de MySQL                                   | `root`                   |
| `DB_PASSWORD`         | Contraseña de MySQL                                | `tu_contraseña`          |
| `DB_NAME`             | Nombre de la base de datos                         | `restaurante`            |
| `DB_PORT`             | Puerto de MySQL                                    | `3306`                   |
| `MAIL_USERNAME`       | Email del restaurante (Gmail)                      | `flamejbresto@gmail.com` |
| `MAIL_PASSWORD`       | Contraseña de aplicación de Gmail (16 caracteres)  | `xxxx xxxx xxxx xxxx`    |
| `MAIL_DEFAULT_SENDER` | Email desde donde se envían los mails              | `flamejbresto@gmail.com` |
| `FRONTEND_URL`        | URL donde corre el frontend                        | `http://localhost:5000`  |

### `frontend/.env`

| Variable       | Descripción                               | Ejemplo                 |
|----------------|-------------------------------------------|-------------------------|
| `API_BASE_URL` | URL base de la API del backend            | `http://localhost:5001` |
| `SECRET_KEY`   | Clave secreta que usa flask para el login | `Clave_secreta`         | 
## Páginas del sitio

### Zona pública (clientes)

| Ruta                         | Descripción                                                    |
|------------------------------|----------------------------------------------------------------|
| `/`                          | Página principal con menú, reseñas, servicios extra y reservas |
| `/reservas` (POST)           | Envío del formulario de reserva                                |
| `/crear/reseña/<id_reserva>` | Formulario para dejar una reseña (accedido desde el email)     |
| `/resena` (POST)             | Envío de la reseña                                             |

### Zona de administración

El panel de administración, para acceder, ir directamente a `http://localhost:5000/login`.

| Ruta                          | Descripción                                                  |
|-------------------------------|--------------------------------------------------------------|
| `/login`                      | Inicio de sesión del administrador                           |
| `/admin`                      | Dashboard principal con estadísticas y gráfico semanal       |
| `/admin/reservas`             | Gestión de reservas (confirmar asistencia, editar, cancelar) |
| `/admin/menu`                 | ABM del menú (alta, baja lógica, modificación)               |
| `/admin/servicios`            | ABM de servicios extra (alta, baja lógica, modificación)     |
| `/admin/resenas`              | Listado y eliminación de reseñas                             |
| `/admin/resenas/estadisticas` | Gráfico de promedio de puntaje mensual                       |
| `/admin/scanner`              | Escáner de códigos QR para validar asistencia                |

## Flujo de una reserva

```
Cliente completa el formulario
        |
        v
Backend genera token UUID → guarda en BD → envía email con QR
        |
        v
Cliente llega al restaurante con el QR
        |
        v
Admin escanea el QR desde /admin/scanner
        |
        v
Backend valida token → estado: "asistio" → envía email con link de reseña
        |
        v
Cliente completa la reseña → se guarda en BD → impacta en el dashboard
```

## Emails automáticos

El sistema envía emails automáticos en los siguientes eventos:

| Evento                               | Destinatario | Contenido                               |
|--------------------------------------|--------------|-----------------------------------------|
| Reserva creada                       | Cliente      | Confirmación + código QR adjunto        |
| Asistencia confirmada (QR escaneado) | Cliente      | Agradecimiento + link para dejar reseña |
| Reserva cancelada                    | Cliente      | Notificación de cancelación             |
| Cancelación desde el email           | Cliente      | Página de confirmación de baja          |

## Endpoints de la API

Base URL: `http://localhost:5001`

### Autenticación
| Método | URL            | Descripción                |
|--------|----------------|----------------------------|
| POST   | `/auth/login`  | Autenticar administrador   |

### Menú
| Método | URL            | Descripción              |
|--------|----------------|--------------------------|
| GET    | `/platos`      | Listar todos los platos  |
| POST   | `/platos`      | Crear un plato           |
| PUT    | `/platos/<id>` | Modificar un plato       |
| DELETE | `/platos/<id>` | Eliminar un plato        |

### Reservas
| Método | URL                          | Descripción                              |
|--------|------------------------------|------------------------------------------|
| GET    | `/reservas/admin`            | Listar todas las reservas                |
| GET    | `/reservas/<id>`             | Obtener una reserva por ID               |
| POST   | `/reservas`                  | Crear una reserva y enviar QR por email  |
| PUT    | `/reservas/<id>`             | Modificar una reserva                    |
| DELETE | `/reservas/<id>`             | Cancelar una reserva                     |
| POST   | `/reservas/verificar_qr`     | Validar QR al momento de la asistencia   |
| GET    | `/reservas/cancelar/<token>` | Cancelar reserva desde el link del email |

### Reseñas
| Método | URL                        | Descripción                                        |
|--------|----------------------------|----------------------------------------------------|
| GET    | `/reseñas`                 | Listar reseñas con paginación y filtro por email   |
| POST   | `/reseñas`                 | Crear una reseña                                   |
| DELETE | `/reseñas/<id>`            | Eliminar una reseña                                |
| GET    | `/reseñas/grafico-resenas` | Promedio mensual de puntajes por año               |
| GET    | `/reseñas/promedio`        | Promedio general de puntaje                        |

### Servicios Extra
| Método | URL                                       | Descripción                                     |
|--------|-------------------------------------------|-------------------------------------------------|
| GET    |  `/restaurante/servicios-extra`           | Listar servicios activos (vista pública)        |
| GET    | `/restaurante/servicios-extra/<id>`       | Obtener un servicio por ID                      |
| GET    | `/restaurante/admin/servicios-extra`      | Listar todos los servicios (admin)              |
| POST   | `/restaurante/admin/servicios-extra`      | Crear un servicio extra                         |
| PATCH  | `/restaurante/admin/servicios-extra/<id>` | Modificar descripción y estado activo/inactivo  |
| DELETE | `/restaurante/admin/servicios-extra/<id>` | Eliminar un servicio extra                      |

### Dashboard
| Método | URL                          | Descripción                    |
|--------|------------------------------|--------------------------------|
| GET    | `/dashboard/estadisticas`    | Estadísticas del mes actual    |
| GET    | `/dashboard/reservas-semana` | Reservas de los últimos 7 días |

## Dependencias principales

| Librería                 | Uso                                            |
|--------------------------|------------------------------------------------|
| `Flask`                  | Framework web (frontend y backend)             |
| `Flask-Mail`             | Envío de emails con adjuntos                   |
| `mysql-connector-python` | Conexión a MySQL                               |
| `qrcode` + `pillow`      | Generación de imágenes QR en memoria           |
| `bcrypt`                 | Hash de contraseñas de administradores         |
| `requests`               | Comunicación HTTP del frontend hacia la API    |
| `python-dotenv`          | Lectura de variables de entorno desde `.env`   |

## Glosario

| Término                  | Definición                                                                                                                                              |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| Blueprint (Flask)        | Mecanismo para agrupar rutas relacionadas en módulos separados. Cada funcionalidad del sistema tiene su propio blueprint.                               |
| SSR                      | Server-Side Rendering. El HTML se genera en el servidor con Jinja2 y se envía al navegador ya renderizado.                                              |
| Jinja2                   | Motor de templates de Flask para generar HTML dinámico.                                                                                                 |
| requests                 | Librería Python que permite hacer llamadas HTTP. El frontend la usa para consumir la API del backend.                                                   |
| Baja lógica              | Técnica que marca un registro como inactivo (`activo = False`) en lugar de eliminarlo físicamente de la base de datos. Usada en menú y servicios extra. |
| Token QR                 | UUID v4 generado al crear una reserva, embebido en el código QR y almacenado en la BD para su validación posterior.                                     |
| HATEOAS                  | Estilo de API REST donde las respuestas incluyen links de navegación (`next`, `prev`, `first`, `last`) para la paginación.                              |
| Flask-Mail               | Extensión de Flask para envío de emails. Configurada con SMTP de Gmail.                                                                                 |
| Contraseña de aplicación | Credencial específica generada por Google para que aplicaciones externas puedan enviar emails desde una cuenta Gmail con verificación en dos pasos.     |
| ABM                      | Alta, Baja y Modificación. Conjunto de operaciones CRUD sobre una entidad del sistema.                                                                  |
| abort(500)               | Helper de Flask que interrumpe la request y devuelve un error 500 al navegador, mostrando la página
