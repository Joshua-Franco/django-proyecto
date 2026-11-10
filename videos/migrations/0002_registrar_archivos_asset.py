"""
Migración de datos de la app `videos`.

Registra en la base de datos los archivos de media que ya existen en
MEDIA_ROOT (la carpeta `assets` del proyecto): 3 imágenes y 2 videos.
Solo se guardan las rutas relativas, no los archivos en sí.

Depende de `videos.0001_initial` e `images.0001_initial` porque crea
registros en ambas tablas.
"""

from pathlib import Path

from django.conf import settings
from django.db import migrations


# Archivos que ya viven en MEDIA_ROOT, con su título para la API.
ARCHIVOS = [
    ('Imagen', 'dog.jpg', 'Perro'),
    ('Imagen', 'dog1.jpg', 'Perro 1'),
    ('Imagen', 'dog2.jpg', 'Perro 2'),
    ('Video', 'cat.mp4', 'Gato'),
    ('Video', 'cat1.mp4', 'Gato 1'),
]


def registrar_archivos(apps, schema_editor):
    """Crea los registros que apuntan a los archivos existentes en assets."""
    Imagen = apps.get_model('images', 'Imagen')
    Video = apps.get_model('videos', 'Video')

    modelos = {'Imagen': Imagen, 'Video': Video}

    for modelo, nombre_archivo, titulo in ARCHIVOS:
        ruta = Path(settings.MEDIA_ROOT) / nombre_archivo
        if not ruta.exists():
            # Si el archivo no está en disco, se omite el registro.
            continue
        modelos[modelo].objects.get_or_create(
            archivo=nombre_archivo,
            defaults={'titulo': titulo},
        )


def eliminar_registros(apps, schema_editor):
    """Reversa: elimina los registros creados por esta migración."""
    Imagen = apps.get_model('images', 'Imagen')
    Video = apps.get_model('videos', 'Video')

    for modelo, nombre_archivo, _titulo in ARCHIVOS:
        modelo_destino = Imagen if modelo == 'Imagen' else Video
        modelo_destino.objects.filter(archivo=nombre_archivo).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(registrar_archivos, eliminar_registros),
    ]
