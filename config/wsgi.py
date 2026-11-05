"""
Punto de entrada WSGI del proyecto.

Permite servir la app con servidores WSGI (Gunicorn, mod_wsgi).
Expone el objeto WSGI como variable de módulo `application`.
"""

import os

from django.core.wsgi import get_wsgi_application

# Indica a Django qué módulo de configuración usar por defecto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
