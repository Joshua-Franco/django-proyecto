from django.db import models
from uuid import uuid4
# Create your models here.
class Tarea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    completado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tareas'