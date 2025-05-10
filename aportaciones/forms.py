from django import forms
from .models import Aportacion

class AportacionForm(forms.ModelForm):
    class Meta:
        model = Aportacion
        fields = ['asociado', 'monto']
