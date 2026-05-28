from django.http import FileResponse
from django.http import FileResponse, HttpResponseNotFound
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Jugador
from .serializer import JugadorSerializer
from .tasks import verificar_modelo_task

from django.conf import settings

import os

class JugadorViewSet(CreateModelMixin, GenericViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer

    def perform_create(self, serializer):
        serializer.save()
        verificar_modelo_task.delay()

def obtener_grafica(request):
    path = os.path.join(settings.BASE_DIR,'static', 'pca_actual.png')

    if not os.path.exists(path): return HttpResponseNotFound("Todavía no existe una gráfica.")

    return FileResponse(open(path, 'rb'),content_type='image/png')