from django.db import models

# Create your models here.
 

class UsuarioModel(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre