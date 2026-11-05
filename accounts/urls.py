"""
Rutas de la app `accounts`.

Mapea las 4 operaciones CRUD de cuentas bajo el prefijo `cuentas/`.
"""

from django.urls import path
from .views import (
    CrearCuentaView,
    ListarCuentasView,
    ObtenerCuentaView,
    ActualizarCuentaView,
    EliminarCuentaView,
    IniciarSesionView,
)

urlpatterns = [
    path('cuentas/crear/', CrearCuentaView.as_view(), name='crear_cuenta'),
    path('cuentas/', ListarCuentasView.as_view(), name='listar_cuentas'),
    path('cuentas/iniciar-sesion/', IniciarSesionView.as_view(), name='iniciar_sesion'),
    path('cuentas/<uuid:pk>/obtener/', ObtenerCuentaView.as_view(), name='obtener_cuenta'),
    path('cuentas/<uuid:pk>/', ActualizarCuentaView.as_view(), name='actualizar_cuenta'),
    path('cuentas/<uuid:pk>/eliminar/', EliminarCuentaView.as_view(), name='eliminar_cuenta'),
]
