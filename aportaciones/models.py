from django.db import models
from asociados.models import Asociado

class Aportacion(models.Model):
    asociado = models.ForeignKey(Asociado, on_delete=models.CASCADE, related_name='aportaciones')
    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='Realizada')

    def __str__(self):
        return f"Aportación Q{self.monto} - {self.asociado.nombre}"

