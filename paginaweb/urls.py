from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('asociados/', include('asociados.urls')),
    path('prestamos/', include('prestamos.urls')),
    path('creditos/', include('creditos.urls')),
    path('aportaciones/', include('aportaciones.urls')),
    path('logout/', views.logout_view, name='logout'),
    path('registrar-empleado/', views.registrar_empleado, name='registrar_empleado'),
    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('empleados/eliminar/<int:pk>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('asociado/', views.panel_asociado, name='panel_asociado'),
    path('asociado/estado-cuenta/', views.generar_estado_cuenta_pdf, name='estado_cuenta_pdf'),
]
