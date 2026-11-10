"""
Rutas de la app `images`.

Subida de imágenes al bucket S3 (`imagenes/crear/`), listado de todas
las imágenes y detalle de una específica.
"""

from django.urls import path
from .views import CrearImagenView, ListarImagenesView, ObtenerImagenView

urlpatterns = [
    path('imagenes/crear/', CrearImagenView.as_view(), name='crear_imagen'),
    path('imagenes/', ListarImagenesView.as_view(), name='listar_imagenes'),
    path('imagenes/<uuid:pk>/', ObtenerImagenView.as_view(), name='obtener_imagen'),
]
