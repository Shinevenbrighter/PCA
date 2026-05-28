# jugadores/urls.py
from django.urls import path
from .views import JugadorViewSet, obtener_grafica

jugador_create = JugadorViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('jugadores/', jugador_create, name='jugador-create'),
    path('grafica/', obtener_grafica, name='obtener-grafica'),
]