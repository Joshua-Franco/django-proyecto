"""
Serializadores de la app `videos`.

Convierten instancias de `Video` a/from JSON para la API REST.

Con `VideoSerializer` se puede SUBIR un video al bucket S3: envía
`multipart/form-data` a `POST /videos/crear/` con los campos `archivo`
(el video) y `titulo` (opcional). django-storages lo sube al bucket en
el mismo `serializer.save()`. El campo `archivo` se serializa como URL
pública del bucket. Django no tiene un campo específico para videos:
se usa `FileField` con validadores de extensión y tamaño.
"""

from pathlib import PurePath

from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from .models import Video

# Tamaño máximo de un video: 500 MB.
MAX_BYTES_VIDEO = 500 * 1024 * 1024

EXTENSIONES_VIDEO = ['mp4', 'webm', 'mkv', 'mov']


def validar_tamano_video(archivo):
    """Validador del campo `archivo`: tamaño máximo 500 MB."""
    if archivo.size > MAX_BYTES_VIDEO:
        mb = MAX_BYTES_VIDEO // (1024 * 1024)
        raise serializers.ValidationError(
            f'El video no debe superar los {mb} MB.'
        )


class VideoSerializer(serializers.ModelSerializer):
    """Serializer DRF del modelo `Video` (lectura + subida al bucket)."""

    titulo = serializers.CharField(max_length=200, required=False, allow_blank=True)
    archivo = serializers.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=EXTENSIONES_VIDEO,
                message='Solo se admiten videos '
                        f'{", ".join(EXTENSIONES_VIDEO)}.',
            ),
            validar_tamano_video,
        ],
    )

    class Meta:
        model = Video
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
