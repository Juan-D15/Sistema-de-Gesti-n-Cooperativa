from django.db import models
from asociados.models import Asociado

class Multa(models.Model):
    asociado = models.ForeignKey(Asociado, on_delete=models.CASCADE, related_name='multas')
    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    motivo = models.TextField(default="Falta de aportación semanal")

    def __str__(self):
        return f"Multa Q{self.monto} - {self.asociado.nombre}"
