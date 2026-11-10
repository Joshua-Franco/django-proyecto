"""
Fixtures compartidas de pytest para todo el proyecto.

pytest descubre este archivo automáticamente: las fixtures están disponibles
en cualquier `tests.py` de las apps sin necesidad de importarlas.
"""

import pytest
from rest_framework.test import APIClient

from images.models import Imagen
from videos.models import Video


@pytest.fixture
def api_client():
    """Cliente HTTP de DRF para llamar a los endpoints del server."""
    return APIClient()


@pytest.fixture
def sample_imagen(db):
    """
    Una imagen de prueba apuntando a la clave `imagenes/dog.jpg` del bucket.
    Usa get_or_create para no duplicar registros si ya existe.
    """
    return Imagen.objects.get_or_create(
        archivo='imagenes/dog.jpg',
        defaults={'titulo': 'Perro'},
    )[0]


@pytest.fixture
def sample_video(db):
    """
    Un video de prueba apuntando a la clave `videos/cat.mp4` del bucket.
    """
    return Video.objects.get_or_create(
        archivo='videos/cat.mp4',
        defaults={'titulo': 'Gato'},
    )[0]
