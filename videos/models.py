"""
Modelos de la app `videos`.

Define el modelo `Video`. Los archivos NO se guardan en disco: se suben
directamente al bucket AWS S3 (django-storages) y la base de datos solo
guarda la clave relativa del objeto (ej. 'videos/cat.mp4').
Django no tiene un campo específico para videos, por eso se usa `FileField`.
"""

from django.db import models
from uuid import uuid4


class Video(models.Model):
    """Modelo de video con identificador UUID."""

    # UUID autogenerado como clave primaria (igual que el modelo `Tarea`).
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    titulo = models.CharField(max_length=200)
    # El archivo se sube al bucket S3 bajo el prefijo videos/.
    archivo = models.FileField(upload_to='videos/')
    # Fecha de creación automática al guardar por primera vez.
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'videos'  # Nombre propio de la tabla en la BD.

    def __str__(self):
        return self.titulo
