
# Create your views here.
import os
import joblib
import numpy as np

from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Jugador
from .serializer import JugadorSerializer
from .tasks import entrenar_pca_si_es_necesario


MODEL_PATH = os.path.join(settings.BASE_DIR, "modelo_pca.pkl")


class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all().order_by("id")
    serializer_class = JugadorSerializer

    def perform_create(self, serializer):
        serializer.save()
        entrenar_pca_si_es_necesario.delay()

    def update(self, request, *args, **kwargs):
        jugador = self.get_object()

        if jugador.entrenado:
            return Response(
                {"error": "No se puede modificar un jugador que ya fue usado para PCA."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        jugador = self.get_object()

        if jugador.entrenado:
            return Response(
                {"error": "No se puede eliminar un jugador que ya fue usado para PCA."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)


@api_view(["GET"])
def puntos_pca(request):
    jugadores = Jugador.objects.filter(entrenado=True)

    data = []

    for jugador in jugadores:
        data.append({
            "id": jugador.id,
            "nombre": jugador.nombre,
            "pca_x": jugador.pca_x,
            "pca_y": jugador.pca_y,
        })

    return Response(data)


@api_view(["POST"])
def obtener_coordenadas(request):
    datos = [
        request.data.get("velocidad"),
        request.data.get("agilidad"),
        request.data.get("fuerza"),
        request.data.get("potencia"),
        request.data.get("edad"),
        request.data.get("peso"),
        request.data.get("altura"),
        request.data.get("partidos_jugados"),
        request.data.get("puntos_anotados"),
        request.data.get("partidos_ganados"),
    ]

    if None in datos:
        return Response(
            {"error": "Faltan datos del jugador."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not os.path.exists(MODEL_PATH):
        return Response(
            {"error": "El modelo PCA todavía no ha sido entrenado."},
            status=status.HTTP_400_BAD_REQUEST
        )

    pca = joblib.load(MODEL_PATH)

    X = np.array([datos], dtype=float)
    coords = pca.transform(X)[0]

    return Response({
        "pca_x": coords[0],
        "pca_y": coords[1]
    })