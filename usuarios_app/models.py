from django.db import models

# Create your models here.
class UserModel(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    document_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    
"""
trigger: active cuando cuando se visite el home => disparar un contador
trigger: active cuando cuando se haga un login => disparar un contador



usuariovisitante
    usuario
    contraseña
    contador

usuarioregistrado
    definir campo

usuarioconsultor
    definir campo

superadmin
    definir campos

"""