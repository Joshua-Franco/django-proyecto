"""
Enrutador raíz del proyecto.

Monta el admin de Django y las rutas de las tres apps (`tasks`, `accounts`,
`api`) directamente en la raíz (`''`), sin prefijo de espacio de nombres.
Las apps definen sus propias rutas (ej. `tareas/`, `cuentas/`).
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('', include('accounts.urls')),
    path('', include('api.urls')),
]
