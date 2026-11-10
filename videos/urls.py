"""
Rutas de la app `videos`.

Subida de videos al bucket S3 (`videos/crear/`), listado de todos los
videos y detalle de uno específico.
"""

from django.urls import path
from .views import CrearVideoView, ListVideoView, ObtenerVideoView

urlpatterns = [
    path('videos/crear/', CrearVideoView.as_view(), name='crear_video'),
    path('videos/', ListVideoView.as_view(), name='lista_video'),
    path('videos/<uuid:pk>/', ObtenerVideoView.as_view(), name='obtener_video'),
]
