from django.db import models
from asociados.models import Asociado

class Prestamo(models.Model):
    asociado = models.ForeignKey(Asociado, on_delete=models.CASCADE, related_name='prestamos')
    fecha_solicitud = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Anulado', 'Anulado')
    ], default='Pendiente')
    interes_mensual = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Préstamo Q{self.monto} - {self.asociado.nombre} ({self.estado})"
