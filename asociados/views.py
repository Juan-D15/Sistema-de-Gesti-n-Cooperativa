from django.shortcuts import render, redirect, get_object_or_404
from .forms import AsociadoForm
from .models import Asociado
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from aportaciones.models import Aportacion
from prestamos.models import Prestamo
from creditos.models import Credito
from multas.models import Multa
from django.contrib.auth.models import User


def registrar_asociado(request):
    if request.method == 'POST':
        form = AsociadoForm(request.POST)
        if form.is_valid():
            asociado = form.save(commit=False)

            # Crear usuario de Django con número de cuenta y PIN
            usuario = User.objects.create_user(
                username=asociado.numero_cuenta,
                password=asociado.pin
            )

            # Vincular usuario al asociado
            asociado.usuario = usuario
            asociado.save()

            return redirect('lista_asociados')
    else:
        form = AsociadoForm()

    return render(request, 'asociados/registro.html', {'form': form})

def registro_exitoso(request):
    return render(request, 'asociados/exito.html')

def lista_asociados(request):
    consulta = request.GET.get('buscar')
    if consulta:
        asociados = Asociado.objects.filter(numero_cuenta__icontains=consulta)
    else:
        asociados = Asociado.objects.all()
    return render(request, 'asociados/lista.html', {'asociados': asociados, 'buscar': consulta})


def editar_asociado(request, pk):
    asociado = get_object_or_404(Asociado, pk=pk)
    if request.method == 'POST':
        form = AsociadoForm(request.POST, instance=asociado)
        if form.is_valid():
            form.save()
            return redirect('lista_asociados')
    else:
        form = AsociadoForm(instance=asociado)
    return render(request, 'asociados/registro.html', {'form': form})

def eliminar_asociado(request, pk):
    asociado = get_object_or_404(Asociado, pk=pk)
    if request.method == 'POST':
        asociado.delete()
        return redirect('lista_asociados')
    return render(request, 'asociados/confirmar_eliminar.html', {'asociado': asociado})

def generar_estado_cuenta(request, pk):
    asociado = Asociado.objects.get(pk=pk)

    aportaciones = Aportacion.objects.filter(asociado=asociado).order_by('-fecha')[:5]
    prestamos = Prestamo.objects.filter(asociado=asociado).order_by('-fecha_solicitud')[:5]
    creditos = Credito.objects.filter(asociado=asociado).order_by('-fecha_solicitud')[:5]
    multas = Multa.objects.filter(asociado=asociado).order_by('-fecha')[:5]

    total_aportaciones = sum(a.monto for a in aportaciones)
    total_prestamos = sum(p.monto for p in prestamos)
    total_creditos = sum(c.monto for c in creditos)
    total_multas = sum(m.monto for m in multas)

    context = {
        'asociado': asociado,
        'aportaciones': aportaciones,
        'prestamos': prestamos,
        'creditos': creditos,
        'multas': multas,
        'total_aportaciones': total_aportaciones,
        'total_prestamos': total_prestamos,
        'total_creditos': total_creditos,
        'total_multas': total_multas,
    }

    template = get_template('asociados/estado_cuenta_pdf.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=estado_cuenta_{asociado.numero_cuenta}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response