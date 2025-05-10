from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Prestamo
from .forms import PrestamoForm


@login_required
def registrar_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)

        if hasattr(request.user, 'asociado'):
            form.fields['asociado'].required = False
            form.fields['asociado'].widget = forms.HiddenInput()

        if form.is_valid():
            prestamo = form.save(commit=False)

            if hasattr(request.user, 'asociado'):
                prestamo.asociado = request.user.asociado

            prestamo.save()
            return redirect('panel_asociado' if hasattr(request.user, 'asociado') else 'lista_prestamos')
    else:
        form = PrestamoForm()
        if hasattr(request.user, 'asociado'):
            form.fields['asociado'].required = False
            form.fields['asociado'].widget = forms.HiddenInput()

    return render(request, 'prestamos/registro.html', {
        'form': form,
        'ocultar_asociado': hasattr(request.user, 'asociado')
    })



def lista_prestamos(request):
    prestamos = Prestamo.objects.all().order_by('-fecha_solicitud')
    return render(request, 'prestamos/lista.html', {'prestamos': prestamos})


def aprobar_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if prestamo.estado == 'Pendiente':
        prestamo.estado = 'Aprobado'
        prestamo.saldo_pendiente = prestamo.monto
        prestamo.asociado.saldo += prestamo.monto
        prestamo.asociado.save()
        prestamo.save()
    return redirect('lista_prestamos')


def anular_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if prestamo.estado == 'Aprobado':
        prestamo.asociado.saldo -= prestamo.monto
        prestamo.asociado.save()
        prestamo.saldo_pendiente = 0
    prestamo.estado = 'Anulado'
    prestamo.save()
    return redirect('lista_prestamos')



