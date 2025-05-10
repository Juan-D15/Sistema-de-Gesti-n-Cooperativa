from django.shortcuts import render, redirect
from .models import Aportacion
from .forms import AportacionForm
from datetime import date
from django.contrib.auth.decorators import login_required
from django import forms

@login_required
def registrar_aportacion(request):
    if request.method == 'POST':
        form = AportacionForm(request.POST)

        if hasattr(request.user, 'asociado'):
            form.fields['asociado'].required = False
            form.fields['asociado'].widget = forms.HiddenInput()

        if form.is_valid():
            aportacion = form.save(commit=False)

            if hasattr(request.user, 'asociado'):
                aportacion.asociado = request.user.asociado

            aportacion.save()
            return redirect('panel_asociado' if hasattr(request.user, 'asociado') else 'lista_aportaciones')
    else:
        form = AportacionForm()
        if hasattr(request.user, 'asociado'):
            form.fields['asociado'].required = False
            form.fields['asociado'].widget = forms.HiddenInput()

    return render(request, 'aportaciones/registro.html', {
        'form': form,
        'ocultar_asociado': hasattr(request.user, 'asociado')
    })


def lista_aportaciones(request):
    aportaciones = Aportacion.objects.all()
    return render(request, 'aportaciones/lista.html', {'aportaciones': aportaciones})