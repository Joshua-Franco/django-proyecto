"""
Serializadores de la app `accounts`.

Convierten instancias de `Cuenta` a/from JSON para la API REST.
"""

from rest_framework import serializers
from .models import Cuenta


class CuentaSerializer(serializers.ModelSerializer):
    """Serializer DRF del modelo `Cuenta` (todos los campos)."""

    class Meta:
        model = Cuenta
        fields = ['id', 'nombre', 'correo_electronico', 'fecha_creacion', 'activo']
