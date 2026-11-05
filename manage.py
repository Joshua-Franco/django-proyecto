#!/usr/bin/env python
"""
Utilidad de línea de comandos de Django.

Punto de entrada para ejecutar comandos de gestión:
`python manage.py <comando>` (runserver, migrate, createsuperuser, etc.).
"""

import os
import sys


def main():
    """Ejecuta un comando de gestión de Django."""
    # Selecciona el módulo de configuración del proyecto.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
