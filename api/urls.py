"""
Rutas de la app `api`.

Monta el health-check en la raíz (`''`), la landing por defecto del sitio.
"""

from django.urls import path
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view()),
]
