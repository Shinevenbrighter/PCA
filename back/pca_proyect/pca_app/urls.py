from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JugadorViewSet, puntos_pca, obtener_coordenadas

router = DefaultRouter()
router.register(r"jugadores", JugadorViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/pca-points/", puntos_pca),
    path("api/coordenadas/", obtener_coordenadas),
]