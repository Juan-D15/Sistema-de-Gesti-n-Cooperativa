from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_aportacion, name='registrar_aportacion'),
    path('lista/', views.lista_aportaciones, name='lista_aportaciones'),
]
