"""
Migración de datos de la app `videos`.

Adecúa las rutas de media a la nueva estructura de `assets/`: los archivos
viven ahora en subcarpetas (`assets/imagenes/`, `assets/videos/`), así que
los registros pasan de 'dog.jpg' a 'imagenes/dog.jpg', etc.
"""

from django.db import migrations

# Mapa de rutas viejas (raíz de assets/) -> nuevas (subcarpetas).
RUTAS_NUEVAS = {
    'dog.jpg': 'imagenes/dog.jpg',
    'dog1.jpg': 'imagenes/dog1.jpg',
    'dog2.jpg': 'imagenes/dog2.jpg',
    'cat.mp4': 'videos/cat.mp4',
    'cat1.mp4': 'videos/cat1.mp4',
}


def renombrar_rutas(apps, schema_editor):
    """Actualiza `archivo` en Imagen y Video con las rutas en subcarpetas."""
    Imagen = apps.get_model('images', 'Imagen')
    Video = apps.get_model('videos', 'Video')

    for vieja, nueva in RUTAS_NUEVAS.items():
        Imagen.objects.filter(archivo=vieja).update(archivo=nueva)
        Video.objects.filter(archivo=vieja).update(archivo=nueva)


def restaurar_rutas(apps, schema_editor):
    """Reversa: vuelve a las rutas planas (archivos en la raíz de assets)."""
    Imagen = apps.get_model('images', 'Imagen')
    Video = apps.get_model('videos', 'Video')

    for vieja, nueva in RUTAS_NUEVAS.items():
        Imagen.objects.filter(archivo=nueva).update(archivo=vieja)
        Video.objects.filter(archivo=nueva).update(archivo=vieja)


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('videos', '0002_registrar_archivos_asset'),
    ]

    operations = [
        migrations.RunPython(renombrar_rutas, restaurar_rutas),
    ]
