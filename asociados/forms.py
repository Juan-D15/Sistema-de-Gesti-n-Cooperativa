from django import forms
from .models import Asociado
from django.core.exceptions import ValidationError
import re

class AsociadoForm(forms.ModelForm):
    class Meta:
        model = Asociado
        fields = ['numero_cuenta', 'nombre', 'saldo', 'pin']
        widgets = {
            'numero_cuenta': forms.TextInput(attrs={
                'maxlength': '10',
                'required': True,
                'class': 'form-control',
                'pattern': r'\d+',
                'title': 'Solo se permiten números'
            }),
            'nombre': forms.TextInput(attrs={
                'maxlength': '100',
                'required': True,
                'class': 'form-control',
                'pattern': r'[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+',
                'title': 'Solo letras y espacios'
            }),
            'saldo': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'required': True,
                'class': 'form-control'
            }),
            'pin': forms.TextInput(attrs={
                'maxlength': '6',
                'required': True,
                'class': 'form-control',
                'pattern': r'\d+',
                'title': 'Solo se permiten números'
            }),
        }

    def clean_numero_cuenta(self):
        numero_cuenta = self.cleaned_data['numero_cuenta']
        if Asociado.objects.filter(numero_cuenta=numero_cuenta).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ya existe un asociado con ese número de cuenta.")
        return numero_cuenta

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre

    def clean_pin(self):
        pin = self.cleaned_data['pin']
        if not pin.isdigit():
            raise ValidationError("El PIN debe contener solo números.")
        if len(pin) > 6:
            raise ValidationError("El PIN no puede tener más de 6 caracteres.")
        return pin