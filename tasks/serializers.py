"""
Serializadores de la app `tasks`.

Convierten instancias de `Tarea` a/from JSON para la API REST.
"""

from rest_framework import serializers
from .models import Tarea


class TareaSerializer(serializers.ModelSerializer):
    """Serializer DRF del modelo `Tarea` (todos los campos)."""

    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'descripcion', 'completado', 'fecha_creacion']
