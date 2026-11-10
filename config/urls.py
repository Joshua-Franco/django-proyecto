"""
Enrutador raíz del proyecto.

Monta el admin de Django y las rutas de las apps (`tasks`, `accounts`,
`health`, `images`, `videos`) directamente en la raíz (`''`), sin prefijo
de espacio de nombres. Las apps definen sus propias rutas
(ej. `tareas/`, `health/`, `imagenes/`).
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('', include('accounts.urls')),
    path('', include('health.urls')),
    path('', include('images.urls')),
    path('', include('videos.urls')),
]
