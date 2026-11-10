"""
Rutas de la app `health`.

Monta el health-check SOLO en la raíz (`''`, la landing del server):
GET / devuelve {"servidor": "okay"}.
"""

from django.urls import path
from .views import HealthView

urlpatterns = [
    path('', HealthView.as_view(), name='inicio'),
]
