"""
Cuarta Forma Normal (4FN):
Una tabla está en 4FN si:

Está en FNBC.
No tiene dependencias multivaluadas.

Una dependencia multivaluada ocurre cuando la presencia de un valor en una columna implica la presencia de uno o más valores en otra columna, independientemente de los otros atributos.
Ejemplo: En una tabla de Empleados_Habilidades_Proyectos, si un empleado tiene múltiples habilidades y trabaja en múltiples proyectos, pero las habilidades no están relacionadas con los proyectos específicos, esto indicaría una dependencia multivaluada. Se resolvería separando en tablas Empleados_Habilidades y Empleados_Proyectos.
"""
class Preferencia(models.Model):
    nombre = models.CharField(max_length=100)

class InquilinoPreferencia(models.Model):
    inquilino = models.ForeignKey(Inquilino, on_delete=models.CASCADE)
    preferencia = models.ForeignKey(Preferencia, on_delete=models.CASCADE)