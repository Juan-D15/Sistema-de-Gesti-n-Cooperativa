from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Credito
from .forms import CreditoForm

@login_required
def registrar_credito(request):
    if request.method == 'POST':
        form = CreditoForm(request.POST)

        if hasattr(request.user, 'asociado'):
            form.fields['asociado'].required = False
            form.fields['asociado'].widget = forms.HiddenInput()

        if form.is_valid():
            credito = form.save(commit=False)

            if hasattr(request.user, 'asociado'):
                credito.asociado = request.user.asociado

            credito.save()
            return redirect('panel_asociado' if hasattr(request.user, 'asociado') else 'lista_creditos')
    else:
        form = CreditoForm()
        if hasattr(request.user, 'asociado'):
            form.fields['asociado'].required = False
            form.fields['asociado'].widget = forms.HiddenInput()

    return render(request, 'creditos/registro.html', {
        'form': form,
        'ocultar_asociado': hasattr(request.user, 'asociado')
    })

def lista_creditos(request):
    creditos = Credito.objects.all().order_by('-fecha_solicitud')
    return render(request, 'creditos/lista.html', {'creditos': creditos})


def aprobar_credito(request, pk):
    credito = get_object_or_404(Credito, pk=pk)
    if credito.estado == 'Pendiente':
        credito.estado = 'Aprobado'
        credito.asociado.saldo += credito.monto
        credito.asociado.save()
        credito.save()
    return redirect('lista_creditos')


def anular_credito(request, pk):
    credito = get_object_or_404(Credito, pk=pk)
    if credito.estado == 'Aprobado':
        credito.asociado.saldo -= credito.monto
        credito.asociado.save()
    credito.estado = 'Anulado'
    credito.save()
    return redirect('lista_creditos')
