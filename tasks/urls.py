"""
Rutas de la app `tasks`.

Mapea las 4 operaciones CRUD de tareas bajo el prefijo `tareas/`.
"""

from django.urls import path
from .views import CrearTareaView, ListarTareasView, ActualizarTareaView, EliminarTareaView

urlpatterns = [
    path('tareas/crear/', CrearTareaView.as_view(), name='crear_tarea'),
    path('tareas/', ListarTareasView.as_view(), name='listar_tareas'),
    path('tareas/<uuid:pk>/', ActualizarTareaView.as_view(), name='actualizar_tarea'),
    path('tareas/<uuid:pk>/eliminar/', EliminarTareaView.as_view(), name='eliminar_tarea'),
]
