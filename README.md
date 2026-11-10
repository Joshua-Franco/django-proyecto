# django-proyecto

API REST pura (sin frontend HTML) construida con Django y Django REST
Framework. Gestiona tareas, cuentas de usuario y **media de imágenes y
videos servida exclusivamente desde un bucket AWS S3** (`django-proyecto`,
región `us-east-2` vía django-storages): el backend no guarda ni sirve
archivos en su disco.

## Stack tecnológico

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.14 | Lenguaje |
| Django | 6.1.3 | Framework web |
| Django REST Framework | 3.18.3 | API REST (serializers, APIViews) |
| djangorestframework-simplejwt | 5.5.1 | Autenticación JWT |
| django-storages | 1.14.6 (+ boto3 1.43) | Storage de media en AWS S3 |
| PostgreSQL | 18.6 | Base de datos (vía psycopg 3.3.8) |
| Pillow | 13.0.0 | Validación de imágenes (`ImageField`) |
| python-dotenv | 1.2.4 | Carga del archivo `.env` |

(Las versiones corresponden al entorno virtual local `venv/`.)

## Estructura del proyecto

```
django-proyecto/
├── config/          # Configuración del proyecto (settings, urls raíz)
├── tasks/           # CRUD de tareas (tareas/)
├── accounts/        # Gestión de cuentas de usuario (cuentas/)
├── health/          # Health-check del server (health/)
├── images/          # Subida + listado + detalle de imágenes (imagenes/)
├── videos/          # Subida + listado + detalle de videos (videos/)
├── manage.py
├── Dockerfile       # Imagen de la app (python:3.14-slim + runserver)
├── docker-compose.yml  # App Django + PostgreSQL en Docker
├── .dockerignore
├── pytest.ini       # Configuración de pytest
├── conftest.py      # Fixtures compartidas de pytest
└── requirements.txt
```

> **Nota:** NO existe carpeta de media en el repo. El media vive solo
> en el bucket S3; la base de datos guarda la clave relativa
> (`imagenes/dog.jpg`, `videos/cat.mp4`) y la API devuelve URLs públicas
> `https://django-proyecto.s3.us-east-2.amazonaws.com/...`.

## Instalación

```bash
# 1. Clonar el repositorio y entrar a la carpeta
cd django-proyecto

# 2. Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows (Git Bash: source venv/Scripts/activate)

# 3. Instalar dependencias
pip install -r requirements.txt
```

> **Requisitos:** PostgreSQL corriendo en 5432 y un bucket S3 con la
> política pública de lectura descrita más abajo.

## Configuración

### Variables de entorno

Crea un archivo `.env` junto a `manage.py` (se ignora en git):

```env
HOST=localhost
NAME=database
USER=postgres
PASSWORD=tu_contraseña
PORT=5432

# --- AWS S3 (única fuente de media) ---
AWS_ACCESS_KEY_ID=...                # access key de IAM
AWS_SECRET_ACCESS_KEY=...            # secret correspondiente
AWS_STORAGE_BUCKET_NAME=django-proyecto
AWS_S3_REGION_NAME=us-east-2
```

El `.env` se carga automáticamente con `python-dotenv`. **Las credenciales
de AWS nunca van en el código, el README, el Dockerfile o el compose.**

### Base de datos

```sql
CREATE DATABASE database;
```

### Migraciones

```bash
python manage.py migrate
```

## Media: el server solo obtiene y sube a AWS S3

- **Nada de disco:** no hay `/media/` local ni carpeta de media en el
  repo; pedir `/media/cualquier-cosa` devuelve 404.
- **Lectura:** los JSON de `/imagenes/` y `/videos/` incluyen la URL
  pública del bucket en el campo `archivo` (sin firma
  `AWS_QUERYSTRING_AUTH=False`). Ej:

  ```
  https://django-proyecto.s3.us-east-2.amazonaws.com/imagenes/dog.jpg
  ```

- **La BD guarda la clave** (`imagenes/dog.jpg`); el URL se construye con
  el dominio explícito `AWS_S3_CUSTOM_DOMAIN` regional (us-east-2).
- **No sobreescripción:** subir un archivo con nombre repetido agrega un
  sufijo aleatorio (`AWS_S3_FILE_OVERWRITE=False`).
- **Credenciales:** solo del `.env`; en Docker se inyectan en runtime
  por interpolación de variables.

### Preparar AWS por primera vez

1. **Rotar credenciales** (si alguna key se compartió): IAM Console →
   Users → Security credentials. Permisos mínimos:
   `s3:GetObject`, `s3:PutObject`, `s3:ListBucket` del bucket de media.
2. **Bucket público de lectura** (URLs públicas): desactivar "Block all
   public access" del bucket `django-proyecto` y aplicar política:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Principal": "*",
       "Action": "s3:GetObject",
       "Resource": "arn:aws:s3:::django-proyecto/*"
     }]
   }
   ```

3. **Seed opcional** de los archivos históricos con AWS CLI:

   ```bash
   aws s3 cp --recursive --content-type "image/jpeg" \
       ./mi-carpeta-local / s3://django-proyecto/imagenes/
   aws s3 cp --recursive --content-type "video/mp4" \
       ./mi-carpeta-videos / s3://django-proyecto/videos/
   ```

4. Poner la clave rotada en `.env` y arrancar (`runserver` o Docker).

## Subir media con Django

### Con la API (multipart/form-data)

Los archivos pasan por el backend y django-storages los sube al bucket:

| Método | Ruta | Campos multipart | Reglas |
|---|---|---|---|
| POST | `/imagenes/crear/` | `archivo` (required), `titulo` (opcional) | Imagen real (PIL), ext. `jpg/jpeg/png/gif/webp`, máx. 10 MB |
| POST | `/videos/crear/` | `archivo` (required), `titulo` (opcional) | Ext. `mp4/webm/mkv/mov`, máx. 500 MB |

Si no envías `titulo`, se deduce del nombre del archivo. Respuesta 201
con id, título, ``archivo`` (URL del bucket) y `fecha_creacion`.

Ejemplo en Windows con curl:

```bash
curl -X POST http://localhost:8000/imagenes/crear/ \
     -F "archivo=@C:/ruta/gato.jpg"
curl -X POST http://localhost:8000/videos/crear/ \
     -F "archivo=@C:/ruta/michi.mp4" -F "titulo=Michi corre"
```

### Auto subida en runtime

Al subir un archivo con el nombre `gato.jpg`, django-storages crea en el
bucket el objeto `imagenes/gato.jpg` (`upload_to='imagenes/'` en el
modelo `Imagen`, `videos/...` en `Video`) y la BD registra esa clave.

## Docker

Todo corre en contenedores: la app Django (Dockerfile, runserver) + un
PostgreSQL propio en red interna.

| Componente | Contenido |
|---|---|
| `Dockerfile` | Imagen `python:3.14-slim`, `tzdata` (America/Lima), HEALTHCHECK de `/`, CMD: `migrate` + `runserver 0.0.0.0:8000` |
| `docker-compose.yml` | `web` (app) + `db` (`postgres:18-alpine`, volumen persistente, healthcheck `pg_isready`) |
| `.dockerignore` | Excluye `venv/`, `.git/`, `.env` (credenciales jamás en la imagen) |

```bash
docker compose up --build     # primera vez: crea imagen + corre migraciones
```

Las credenciales AWS viajan por interpolación `${VAR}` al runtime; el
compose falla con mensaje claro si `PASSWORD`, `AWS_ACCESS_KEY_ID` o
`AWS_SECRET_ACCESS_KEY` no están en el `.env`.

| Puerto | Qué es |
|---|---|
| 8000 | App Django (`web`) |
| 5432 | Tu PostgreSQL local (fuera de Docker) |
| 5433 | PostgreSQL del compose (`db`), para inspección externa |

```bash
docker compose down -v        # apagar y borrar datos del volumen
```

## Ejecutar el servidor (sin Docker)

```bash
python manage.py runserver
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Raíz del server (health-check): `{"servidor": "okay"}` |
| GET | `/tareas/` | Lista de tareas |
| POST | `/tareas/crear/` | Crear tarea |
| GET/PUT/PATCH | `/tareas/<uuid>/` | Detalle/actualizar tarea |
| DELETE | `/tareas/<uuid>/eliminar/` | Eliminar tarea |
| GET | `/cuentas/` | Lista de cuentas activas |
| POST | `/cuentas/crear/` | Crear cuenta |
| GET | `/cuentas/<uuid>/obtener/` | Detalle de una cuenta |
| PUT/PATCH | `/cuentas/<uuid>/` | Actualizar cuenta (requiere token JWT) |
| DELETE | `/cuentas/<uuid>/eliminar/` | Desactivar cuenta (requiere token JWT) |
| POST | `/cuentas/iniciar-sesion/` | Login (devuelve tokens JWT) |
| POST | `/imagenes/crear/` | Subir imagen al bucket (multipart) |
| GET | `/imagenes/` | Lista de imágenes con URLs del bucket |
| GET | `/imagenes/<uuid>/` | Detalle de una imagen |
| POST | `/videos/crear/` | Subir video al bucket (multipart) |
| GET | `/videos/` | Lista de videos con URLs del bucket |
| GET | `/videos/<uuid>/` | Detalle de un video |

Ejemplo de respuesta (en modo S3 las URLs `archivo` apuntan al bucket):

```json
[
  {
    "id": "9f4527df-d66d-4cf4-8e55-53fb712209c0",
    "titulo": "Perro 2",
    "archivo": "https://django-proyecto.s3.us-east-2.amazonaws.com/imagenes/dog2.jpg",
    "fecha_creacion": "2026-11-07 19:44:22"
  }
]
```

Las fechas salen en `America/Lima` con formato
`Año-Mes-Día Hora:Minuto:Segundo` (`DATETIME_FORMAT` de DRF).

### Autenticación

**JWT** (`rest_framework_simplejwt`). Actualizar y eliminar cuentas
exigen token; el resto de vistas no define `permission_classes` (default
de DRF: *AllowAny*). Para las rutas protegidas añade el header:

```
Authorization: Bearer <access_token>
```

## Notas de producción

- `runserver` es el server de desarrollo. Para producción: gunicorn +
  nginx/CloudFront delante; el media ya vive en el bucket S3.
- `SECRET_KEY` y credenciales desde variables de entorno; `DEBUG=False`.

## Gestión de archivos (resumen)

- El backend NO almacena media en disco.
- La BD guarda la clave relativa del objeto en el bucket
  (`imagenes/dog.jpg`, `videos/cat.mp4`).
- La URL pública se arma con `AWS_S3_CUSTOM_DOMAIN`, regiones formato:
  `https://<bucket>.s3.<region>.amazonaws.com/<clave>`.
- Subir nuevas media: endpoints `/imagenes/crear/` y `/videos/crear/`.