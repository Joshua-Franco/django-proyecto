"""
Modelos de la app `accounts`.

Define el modelo `Cuenta`, representación de una cuenta de usuario.
"""

from django.db import models
from uuid import uuid4


class Cuenta(models.Model):
    """Modelo de cuenta con identificador UUID."""

    # UUID autogenerado como clave primaria.
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)  # El correo debe ser único.
    activo = models.BooleanField(default=True)  # False = cuenta desactivada (borrado lógico).
    # Fecha de creación automática al guardar por primera vez.
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cuentas'  # Nombre propio de la tabla en la BD.
