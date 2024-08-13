"""
Forma Normal de Boyce-Codd (FNBC):
Una tabla está en FNBC si:

Está en 3FN.
Para cada dependencia funcional X → Y, X debe ser una superclave.

La FNBC es ligeramente más estricta que la 3FN. Resuelve ciertas anomalías que pueden quedar después de aplicar 3FN en casos donde hay múltiples claves candidatas compuestas que se superponen.
Ejemplo: En una tabla de Cursos (Profesor, Curso, Horario) donde un profesor solo puede enseñar un curso a la vez, pero un curso puede ser enseñado por varios profesores en diferentes horarios, tanto {Profesor, Horario} como {Curso, Horario} podrían ser claves. Esto requeriría una descomposición adicional para cumplir con FNBC.
"""
class RolPropietario(models.Model):
    nombre = models.CharField(max_length=50)  # ej. "administrador", "inversor"

class PropietarioPropiedad(models.Model):
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    rol = models.ForeignKey(RolPropietario, on_delete=models.PROTECT)