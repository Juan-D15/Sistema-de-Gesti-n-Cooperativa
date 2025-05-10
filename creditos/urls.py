from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_credito, name='registrar_credito'),
    path('lista/', views.lista_creditos, name='lista_creditos'),
    path('aprobar/<int:pk>/', views.aprobar_credito, name='aprobar_credito'),
    path('anular/<int:pk>/', views.anular_credito, name='anular_credito'),
]
