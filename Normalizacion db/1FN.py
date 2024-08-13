from django.db import models
"""
Primera Forma Normal (1FN):
Una tabla está en 1FN si:

Cada columna contiene valores atómicos (indivisibles).
No hay grupos repetitivos de columnas.
Existe una clave primaria que identifica de manera única cada fila.

Ejemplo: Convertir una tabla con múltiples números de teléfono en una columna a una tabla separada para números de teléfono.

"""
class Propietario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.PositiveIntegerField(max_length=15)
    email = models.EmailField(unique=True)
    experiencia_inmobiliaria = models.TextField()

class Propiedad(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    rnt = models.CharField(max_length=50)
    capacidad = models.IntegerField()

class Inquilino(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    ocupacion = models.CharField(max_length=100)
    preferencias = models.TextField()

class Habitacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class Reserva(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado_pago = models.CharField(max_length=50)

class EmpresaRemodelacion(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

class ServicioRemodelacion(models.Model):
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()