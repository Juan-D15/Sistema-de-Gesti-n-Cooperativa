from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta
from asociados.models import Asociado
from prestamos.models import Prestamo
from creditos.models import Credito
from aportaciones.models import Aportacion
from prestamos.models import Prestamo
from creditos.models import Credito
from multas.models import Multa
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.conf import settings
from django.template.loader import get_template
from io import BytesIO

def verificar_multas():
    asociados = Asociado.objects.all()
    hoy = date.today()

    for asociado in asociados:
        if (hoy - asociado.fecha_registro).days < 7:
            continue

        ultima_aportacion = Aportacion.objects.filter(asociado=asociado).order_by('-fecha').first()
        if not ultima_aportacion or (hoy - ultima_aportacion.fecha).days > 7:
            if not Multa.objects.filter(asociado=asociado, fecha=hoy).exists():
                Multa.objects.create(asociado=asociado, monto=10.00, fecha=hoy)
                asociado.saldo -= 10
                asociado.save()
            
@login_required
def home(request):
    verificar_multas()

    context = {
        'total_asociados': Asociado.objects.count(),
        'total_aportaciones': Aportacion.objects.count(),
        'total_prestamos': Prestamo.objects.count(),
        'total_creditos': Credito.objects.count(),
        'total_multas': Multa.objects.count(),
    }

    return render(request, 'inicio.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Intentar login como empleado (usuario de Django)
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('home')
            elif hasattr(user, 'asociado'):
                return redirect('panel_asociado')
            return redirect('home')

        # Si falla, intentar como asociado por número de cuenta y pin
        try:
            asociado = Asociado.objects.get(numero_cuenta=username, pin=password)
            login(request, asociado.usuario)
            return redirect('panel_asociado')
        except Asociado.DoesNotExist:
            messages.error(request, 'Credenciales inválidas.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@user_passes_test(lambda u: u.is_superuser)
def registrar_empleado(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe.')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Empleado registrado exitosamente.')
            return redirect('login')
    return render(request, 'registro_empleado.html')


def lista_empleados(request):
    empleados = User.objects.exclude(asociado__isnull=False)
    return render(request, 'empleados/lista.html', {'empleados': empleados})

@user_passes_test(lambda u: u.is_superuser)
def eliminar_empleado(request, pk):
    empleado = get_object_or_404(User, pk=pk)
    if empleado != request.user:  # Evita que el admin se elimine a sí mismo
        empleado.delete()
    return redirect('lista_empleados')

@login_required
def panel_asociado(request):
    asociado = request.user.asociado
    prestamos = Prestamo.objects.filter(asociado=asociado).order_by('-fecha_solicitud')[:5]
    creditos = Credito.objects.filter(asociado=asociado).order_by('-fecha_solicitud')[:5]
    aportaciones = Aportacion.objects.filter(asociado=asociado).order_by('-fecha')[:5]

    return render(request, 'asociados/panel.html', {
        'prestamos': prestamos,
        'creditos': creditos,
        'aportaciones': aportaciones,
    })
    

@login_required
def generar_estado_cuenta_pdf(request):
    if not hasattr(request.user, 'asociado'):
        return HttpResponse("No autorizado", status=403)

    asociado = request.user.asociado

    aportaciones = Aportacion.objects.filter(asociado=asociado)
    prestamos = Prestamo.objects.filter(asociado=asociado)
    creditos = Credito.objects.filter(asociado=asociado)
    multas = Multa.objects.filter(asociado=asociado) if 'multas' in settings.INSTALLED_APPS else []

    template = get_template('asociados/estado_cuenta.html')
    context = {
        'asociado': asociado,
        'aportaciones': aportaciones,
        'prestamos': prestamos,
        'creditos': creditos,
        'multas': multas,
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response, encoding='UTF-8')
    return response