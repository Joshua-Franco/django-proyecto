"""
Configuración del proyecto Django (paquete `config`).

Contiene la configuración global: apps instaladas, middleware, base de datos
PostgreSQL (lee credenciales desde variables de entorno en `.env`),
validadores de contraseña, y autenticación JWT (simplejwt).
"""

from datetime import timedelta
from pathlib import Path
from os import getenv
from dotenv import load_dotenv
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
}

# Ruta raíz del proyecto (carpeta que contiene manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga las variables de entorno del archivo `.env` (credenciales de la BD).
load_dotenv(BASE_DIR / '.env')

# Production configuration is injected by Render; local development can use .env.
DEBUG = getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
SECRET_KEY = getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('Define SECRET_KEY en el entorno.')

ALLOWED_HOSTS = [
    host.strip()
    for host in getenv('ALLOWED_HOSTS', '').split(',')
    if host.strip()
]
render_hostname = getenv('RENDER_EXTERNAL_HOSTNAME')
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

# Apps de Django + apps propias del proyecto + DRF + simplejwt.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'tasks',
    'accounts',
    'health',
    'images',
    'videos',
    'storages',
]

# Cadena de middleware estándar de Django (seguridad, sesiones, CSRF, etc.).
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Módulo que define las URLs raíz del proyecto.
ROOT_URLCONF = 'config.urls'

# Configuración de plantillas. No hay plantillas HTML: es una API REST pura.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Aplicación WSGI para despliegue con servidores como Gunicorn.
WSGI_APPLICATION = 'config.wsgi.application'

# Base de datos PostgreSQL: DATABASE_URL puede venir del entorno o del .env local.
# Se quitan comillas que python-dotenv pueda conservar.
_DATABASE_URL = getenv("DATABASE_URL", "").strip('"').strip("'")
if not _DATABASE_URL:
    raise ImproperlyConfigured('Define DATABASE_URL en el entorno.')

DATABASES = {
    "default": dj_database_url.parse(
        _DATABASE_URL,
        conn_max_age=600,
        ssl_require=True
    )
}

# Validadores de fortaleza de contraseña para el auth de Django.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Idioma y zona horaria del proyecto.
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# Prefijo para archivos estáticos (no aplica: es una API sin frontend).
STATIC_URL = 'static/'

# --- Storage de media: SOLO AWS S3 ---
# El backend NO guarda ni sirve archivos desde el disco: las imágenes y
# videos se obtienen y se suben directamente al bucket S3 del `.env`
# (django-storages). La BD solo almacena la clave relativa (ej.
# 'imagenes/dog.jpg'); las URLs públicas del bucket son las que se
# serializan en los JSON de la API.
AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = getenv('AWS_S3_REGION_NAME')

STORAGES = {
    'default': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage'},
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

# Dominio explícito y regional para las URLs públicas del bucket.
AWS_S3_CUSTOM_DOMAIN = (
    f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
)
# URL pública directa del bucket, sin firmas ni querystring.
AWS_QUERYSTRING_AUTH = False
# No sobreescribe archivos con el mismo nombre: sube dog.jpg repetido
# como dog_A1B2C3D4.jpg.
AWS_S3_FILE_OVERWRITE = False
# Sin gestión de ACL (compatible con Object Ownership "Bucket owner
# enforced" y la política pública de lectura del bucket).
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

# Autenticación JWT por defecto para toda la API (simplejwt).
# DATETIME_FORMAT: las fechas de la API salen como "año-mes-día hora:minuto:segundo"
# (convertidas a la zona horaria activa: America/Lima).
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
}

# Configuración de correo: los correos se imprimen en la consola (desarrollo).
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
