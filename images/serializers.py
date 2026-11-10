"""
Serializadores de la app `images`.

Convierten instancias de `Imagen` a/from JSON para la API REST.

Con `ImagenSerializer` también se puede SUBIR una imagen al bucket S3:
envía `multipart/form-data` a `POST /imagenes/crear/` con los campos
`archivo` (la imagen) y `titulo` (opcional). DRF valida el contenido
con PIL y django-storages lo sube al bucket en el mismo `serializer.save()`.
El campo `archivo` se serializa como URL pública del bucket.
"""

from pathlib import PurePath

from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from .models import Imagen

# Tamaño máximo de una imagen: 10 MB.
MAX_BYTES_IMAGEN = 10 * 1024 * 1024

EXTENSIONES_IMAGEN = ['jpg', 'jpeg', 'png', 'gif', 'webp']


def validar_tamano_imagen(archivo):
    """Validador del campo `archivo`: tamaño máximo 10 MB."""
    if archivo.size > MAX_BYTES_IMAGEN:
        mb = MAX_BYTES_IMAGEN // (1024 * 1024)
        raise serializers.ValidationError(
            f'La imagen no debe superar los {mb} MB.'
        )


class ImagenSerializer(serializers.ModelSerializer):
    """Serializer DRF del modelo `Imagen` (lectura + subida al bucket)."""

    titulo = serializers.CharField(max_length=200, required=False, allow_blank=True)
    archivo = serializers.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=EXTENSIONES_IMAGEN,
                message='Solo se admiten imágenes '
                        f'{", ".join(EXTENSIONES_IMAGEN)}.',
            ),
            validar_tamano_imagen,
        ],
    )

    class Meta:
        model = Imagen
        fields = ['id', 'titulo', 'archivo', 'fecha_creacion']

    def validate(self, attrs):
        """Título opcional: si falta, se deduce del nombre del archivo."""
        if not attrs.get('titulo'):
            archivo = attrs.get('archivo')
            if archivo is not None and hasattr(archivo, 'name'):
                attrs['titulo'] = PurePath(archivo.name).stem[:200]
            else:
                raise serializers.ValidationError(
                    {'titulo': 'El título no puede ir vacío.'}
                )
        return attrs
