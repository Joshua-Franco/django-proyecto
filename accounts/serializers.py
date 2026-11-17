"""
Serializadores de la app `accounts`.

Convierten instancias de `Cuenta` a/from JSON para la API REST.
"""

import bcrypt
from rest_framework import serializers

from .models import Cuenta


class CuentaSerializer(serializers.ModelSerializer):
    """Serializer DRF del modelo `Cuenta` (todos los campos)."""

    class Meta:
        model = Cuenta
        fields = ['id', 'nombre', 'correo_electronico', 'fecha_creacion', 'activo']


class CrearCuentaSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=8, trim_whitespace=False
    )

    class Meta:
        model = Cuenta
        fields = ['id', 'nombre', 'correo_electronico', 'password', 'fecha_creacion', 'activo']

    def validate_password(self, value):
        if len(value.encode('utf-8')) > 72:
            raise serializers.ValidationError(
                'La contraseña no puede superar 72 bytes en UTF-8.'
            )
        return value

    def create(self, validated_data):
        password = validated_data['password'].encode('utf-8')
        validated_data['password'] = bcrypt.hashpw(
            password, bcrypt.gensalt()
        ).decode('ascii')
        return super().create(validated_data)


class IniciarSesionSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    correo_electronico = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_password(self, value):
        if len(value.encode('utf-8')) > 72:
            raise serializers.ValidationError(
                'La contraseña no puede superar 72 bytes en UTF-8.'
            )
        return value
