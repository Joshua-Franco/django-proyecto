"""
Tests del server en sí (config).

Comprueban el health-check, que las rutas principales de la API
responden y que NO hay serving local de media (el backend solo obtiene
las imágenes y videos del bucket AWS S3).
"""

import pytest


@pytest.mark.django_db
def test_rutas_principales_responden(api_client):
    """Las rutas de todas las apps devuelven 200 en JSON."""
    for ruta in ['/', '/tareas/', '/cuentas/', '/imagenes/', '/videos/']:
        response = api_client.get(ruta)
        assert response.status_code == 200, f"GET {ruta} falló"


def test_sin_serving_local_de_media(api_client):
    """
    GET /media/<archivo> devuelve 404: ya no se sirve nada desde el disco.
    Las imágenes y videos solo se obtienen del bucket AWS S3 (las URLs
    del bucket viajan dentro de los JSON de /imagenes/ y /videos/).
    """
    response = api_client.get('/media/imagenes/dog.jpg')
    assert response.status_code == 404
