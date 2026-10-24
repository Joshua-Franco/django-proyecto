from rest_framework import serializers
from .models import Cuenta

class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ['id', 'nombre', 'correo_electronico', 'fecha_creacion']