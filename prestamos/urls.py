from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_prestamo, name='registrar_prestamo'),
    path('lista/', views.lista_prestamos, name='lista_prestamos'),
    path('aprobar/<int:pk>/', views.aprobar_prestamo, name='aprobar_prestamo'),
    path('anular/<int:pk>/', views.anular_prestamo, name='anular_prestamo'),
]
