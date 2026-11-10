"""
Modelos de la app `tasks`.

Define el modelo `Tarea`, la entidad principal del proyecto.
"""

from django.db import models
from uuid import uuid4


class Tarea(models.Model):
    """Modelo de tarea con identificador UUID."""

    # UUID autogenerado como clave primaria (no expone secuencias internas).
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    completado = models.BooleanField(default=False)
    # Fecha de creación automática al guardar por primera vez.
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tareas'  # Nombre propio de la tabla en la BD.
