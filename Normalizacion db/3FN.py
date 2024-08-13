"""
Tercera Forma Normal (3FN):
Una tabla está en 3FN si:

Está en 2FN.
No hay dependencias transitivas de atributos no clave.

Ejemplo: En una tabla de empleados, si el Departamento determina la Ubicación, y el ID_Empleado determina el Departamento, entonces la Ubicación depende transitivamente del ID_Empleado. Esto se resolvería moviendo Ubicación a una tabla de Departamentos.
"""
class EstadoPago(models.Model):
    nombre = models.CharField(max_length=50)

class Reserva(models.Model):
    # ... otros campos ...
    estado_pago = models.ForeignKey(EstadoPago, on_delete=models.PROTECT)