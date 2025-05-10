from django.core.management.base import BaseCommand
from datetime import date, timedelta
from asociados.models import Asociado
from aportaciones.models import Aportacion
from multas.models import Multa

class Command(BaseCommand):
    help = 'Verifica multas semanales por falta de aportaciones'

    def handle(self, *args, **kwargs):
        hoy = date.today()
        inicio_semana = hoy - timedelta(days=hoy.weekday())  # lunes de esta semana

        for asociado in Asociado.objects.all():
            hizo_aporte = Aportacion.objects.filter(
                asociado=asociado,
                fecha__gte=inicio_semana
            ).exists()

            if not hizo_aporte:
                Multa.objects.create(
                    asociado=asociado,
                    fecha=hoy,
                    monto=10.00,
                    motivo="No realizó aportación esta semana"
                )
                asociado.saldo -= 10.00
                asociado.save()
                self.stdout.write(f"Multa generada para: {asociado.nombre}")
