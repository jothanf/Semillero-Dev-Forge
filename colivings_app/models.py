from django.db import models

# Create your models here.
class ColivingModel(models.Model):
    nombre_coliving = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.IntegerField()

    def __str__(self):
        return self.nombre_coliving