"""
Quinta Forma Normal (5FN):
Una tabla está en 5FN si:

Está en 4FN.
No puede ser descompuesta en tablas más pequeñas sin perder información, a menos que esas tablas contengan las claves candidatas de la tabla original.

La 5FN trata con las dependencias de join, que son más sutiles y menos comunes en la práctica.
Ejemplo: Una tabla que relaciona Proveedores, Productos y Proyectos, donde cada combinación tiene un significado específico que no puede derivarse de relaciones binarias entre pares de estas entidades.
"""
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)

class EmpresaServicio(models.Model):
    empresa = models.ForeignKey(EmpresaRemodelacion, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

class PropiedadServicioEmpresa(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    empresa_servicio = models.ForeignKey(EmpresaServicio, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)