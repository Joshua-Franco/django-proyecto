"""
Configuración del proyecto Django (paquete `config`).

Contiene la configuración global: apps instaladas, middleware, base de datos
PostgreSQL (lee credenciales desde variables de entorno en `.env`),
validadores de contraseña, y autenticación JWT (simplejwt).
"""

from datetime import timedelta
from pathlib import Path
from os import getenv

# Ruta raíz del proyecto (carpeta que contiene manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta de Django. En producción debe ir en una variable de entorno,
# nunca hardcodeada. Actualmente es una clave de desarrollo insegura.
SECRET_KEY = 'django-insecure-f9)ovj^u_e#uze!zs^hs+7p0pb2&vxzdgu5%5#6rugo$_&c^rk'

# True en desarrollo (muestra errores detallados). Debe ser False en producción.
DEBUG = True

# Dominios permitidos. Vacío solo sirve para `localhost`/127.0.0.1 en desarrollo.
ALLOWED_HOSTS = []

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
    'api',
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

# Base de datos PostgreSQL. Las credenciales se leen del archivo `.env`
# mediante variables de entorno (HOST, NAME, USER, PASSWORD, PORT).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": getenv("HOST"),
        "NAME": getenv("NAME"),
        "USER": getenv("USER"),
        "PASSWORD": getenv("PASSWORD"),
        "PORT": getenv("PORT"),
    }
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Prefijo para archivos estáticos (no aplica: es una API sin frontend).
STATIC_URL = 'static/'

# Autenticación JWT por defecto para toda la API (simplejwt).
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Vigencia de los tokens JWT.
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# Configuración de correo. Usar `EMAIL_BACKEND` (clave estándar de Django),
# no `MAILERS`. Tal como está, el backend de consola no tiene efecto.
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
