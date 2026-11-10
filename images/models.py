"""
Modelos de la app `images`.

Define el modelo `Imagen`. Los archivos NO se guardan en disco: se suben
directamente al bucket AWS S3 (django-storages) y la base de datos solo
guarda la clave relativa del objeto (ej. 'imagenes/dog.jpg').
"""

from django.db import models
from uuid import uuid4


class Imagen(models.Model):
    """Modelo de imagen con identificador UUID."""

    # UUID autogenerado como clave primaria (igual que el modelo `Tarea`).
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    titulo = models.CharField(max_length=200)
    # El archivo se sube al bucket S3 bajo el prefijo imagenes/.
    archivo = models.ImageField(upload_to='imagenes/')
    # Fecha de creación automática al guardar por primera vez.
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'imagenes'  # Nombre propio de la tabla en la BD.

    def __str__(self):
        return self.titulo
