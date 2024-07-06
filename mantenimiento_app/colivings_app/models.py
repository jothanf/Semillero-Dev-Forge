from django.db import models
from usuarios_app.models import UsuarioModel

# Create your models here.
class ColivingModel(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    propietario = models.ForeignKey(UsuarioModel, on_delete=models.CASCADE, related_name='colivings')
    servicios = models.JSONField(blank=True, null=True)  # Ej. ['WiFi', 'Piscina', 'Gimnasio']
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    foto_perfil = models.ImageField(upload_to='foto_perfil_coliving/', blank=True, null=True)