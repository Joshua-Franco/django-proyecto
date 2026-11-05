"""
Punto de entrada ASGI del proyecto.

Permite servir la app con servidores asíncronos (Uvicorn, Daphne).
Expone el objeto ASGI como variable de módulo `application`.
"""

import os

from django.core.asgi import get_asgi_application

# Indica a Django qué módulo de configuración usar por defecto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
