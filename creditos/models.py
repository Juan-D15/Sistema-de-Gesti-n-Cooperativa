from django.db import models
from asociados.models import Asociado

class Credito(models.Model):
    asociado = models.ForeignKey(Asociado, on_delete=models.CASCADE, related_name='creditos')
    fecha_solicitud = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Anulado', 'Anulado')
    ], default='Pendiente')

    def __str__(self):
        return f"Crédito Q{self.monto} - {self.asociado.nombre} ({self.estado})"
