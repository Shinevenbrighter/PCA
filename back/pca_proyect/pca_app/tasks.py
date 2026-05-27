import os
import joblib
from matplotlib import pyplot as plt
import numpy as np

from celery import shared_task
from django.conf import settings
from sklearn.decomposition import IncrementalPCA

from .models import Jugador 

MODEL_PATH = os.path.join(settings.BASE_DIR, "modelo_pca.pkl")
GRAPH_PATH = os.path.join(settings.BASE_DIR, "static/grafica_pca.png")
pca = IncrementalPCA(n_components=2, batch_size=20)

@shared_task
def entrenar_pca_si_es_necesario():
    pendientes = Jugador.objects.filter(entrenado=False).order_by("id")

    if pendientes.count() < 20:
        return "No hay suficientes jugadores pendientes."

    batch = list(pendientes[:20])

    X = np.array([jugador.valores_pca() for jugador in batch], dtype=float)


    pca.partial_fit(X)

    todos = list(Jugador.objects.all())
    X = np.array([jugador.valores_pca() for jugador in todos], dtype=float)
    coordenadas = pca.transform(X)

    for jugador, coords in zip(todos, coordenadas):
        jugador.pca_x = coords[0]
        jugador.pca_y = coords[1]
        jugador.entrenado = True
        jugador.save()

    #joblib.dump(pca, MODEL_PATH)

    generar_grafica_pca()
    return "PCA actualizado correctamente."



def generar_grafica_pca():
    jugadores = Jugador.objects.all()

    xs = [j.pca_x for j in jugadores]
    ys = [j.pca_y for j in jugadores]
    
    os.makedirs(os.path.dirname(GRAPH_PATH), exist_ok=True)

    plt.figure(figsize=(8, 8))
    plt.scatter(xs, ys)

    plt.title("Incremental PCA de jugadores")
    plt.xlabel("Componente principal 1")
    plt.ylabel("Componente principal 2")
    plt.grid(True)
    plt.savefig(GRAPH_PATH)
    plt.close()
