from django import forms
from .models import Asociado
from django.core.exceptions import ValidationError

class AsociadoForm(forms.ModelForm):
    class Meta:
        model = Asociado
        fields = ['numero_cuenta', 'nombre', 'saldo', 'pin']

    def clean_numero_cuenta(self):
        numero_cuenta = self.cleaned_data['numero_cuenta']
        if Asociado.objects.filter(numero_cuenta=numero_cuenta).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ya existe un asociado con ese número de cuenta.")
        return numero_cuenta
