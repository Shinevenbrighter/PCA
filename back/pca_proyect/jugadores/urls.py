from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    JugadorViewSet,
    obtener_grafica
)

router = DefaultRouter()

router.register(
    r'jugadores',
    JugadorViewSet
)

urlpatterns = [

    path(
        'api/',
        include(router.urls)
    ),

    path(
        'api/grafica/',
        obtener_grafica
    )
]