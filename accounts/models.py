from django.db import models
from uuid import uuid4
# Create your models here.
class Cuenta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cuentas'