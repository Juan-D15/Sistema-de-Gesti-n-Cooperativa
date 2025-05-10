from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_asociado, name='registrar_asociado'),
    path('exito/', views.registro_exitoso, name='registro_exitoso'),
    path('lista/', views.lista_asociados, name='lista_asociados'),
    path('editar/<int:pk>/', views.editar_asociado, name='editar_asociado'),
    path('eliminar/<int:pk>/', views.eliminar_asociado, name='eliminar_asociado'),
    path('estado-cuenta/<int:pk>/', views.generar_estado_cuenta, name='estado_cuenta'),
]
