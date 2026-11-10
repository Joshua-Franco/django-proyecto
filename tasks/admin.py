"""
Registro de modelos en el admin de Django para la app `tasks`.
"""

from django.contrib import admin

from .models import Tarea

admin.site.register(Tarea)
