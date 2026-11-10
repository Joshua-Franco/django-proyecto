"""
Registro de modelos en el admin de Django para la app `accounts`.
"""

from django.contrib import admin

from .models import Cuenta

admin.site.register(Cuenta)
