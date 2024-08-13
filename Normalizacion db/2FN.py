"""
Segunda Forma Normal (2FN):
Una tabla está en 2FN si:

Está en 1FN.
Todos los atributos no clave dependen completamente de la clave primaria (elimina dependencias parciales).

Ejemplo: Si tienes una tabla de pedidos con (ID_Pedido, ID_Producto, Nombre_Producto, Cantidad), el Nombre_Producto depende solo del ID_Producto, no del ID_Pedido completo. Esto se resolvería separando los productos en su propia tabla.
"""
class Propiedad(models.Model):
    # ... campos existentes ...
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)

class Habitacion(models.Model):
    # ... campos existentes ...
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)

class Reserva(models.Model):
    # ... campos existentes ...
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    inquilino = models.ForeignKey(Inquilino, on_delete=models.CASCADE)

class ServicioRemodelacion(models.Model):
    # ... campos existentes ...
    empresa = models.ForeignKey(EmpresaRemodelacion, on_delete=models.CASCADE)
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)