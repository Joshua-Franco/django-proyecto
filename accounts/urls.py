from django.urls import path
from .views import CrearCuentaView, ListarCuentasView, ActualizarCuentaView, EliminarCuentaView

urlpatterns = [
    path('cuentas/crear/', CrearCuentaView.as_view(), name='crear_cuenta'),
    path('cuentas/', ListarCuentasView.as_view(), name='listar_cuentas'),
    path('cuentas/<uuid:pk>/', ActualizarCuentaView.as_view(), name='actualizar_cuenta'),
    path('cuentas/<uuid:pk>/eliminar/', EliminarCuentaView.as_view(), name='eliminar_cuenta'),
]