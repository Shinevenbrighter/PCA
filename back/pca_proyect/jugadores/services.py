import os
import joblib
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import IncrementalPCA

from django.conf import settings

from .models import Jugador

MODEL_PATH = os.path.join(settings.BASE_DIR, 'pca_model.pkl')

GRAPH_PATH = os.path.join(
    settings.BASE_DIR,
    'static',
    'pca_actual.png'
)
def verificar_modelo():

    pendientes = Jugador.objects.filter(
        entrenado=False
    ).order_by('id')

    if pendientes.count() >= 20:
        entrenar_pca()

def entrenar_pca():

    jugadores = list(
        Jugador.objects.filter(
            entrenado=False
        ).order_by('id')[:20]
    )

    X = np.array([
        jugador.vector_pca()
        for jugador in jugadores
    ])

    if os.path.exists(MODEL_PATH):

        pca = joblib.load(MODEL_PATH)

    else:

        pca = IncrementalPCA(
            n_components=2,
            batch_size=20
        )

    pca.partial_fit(X)

    coordenadas = pca.transform(X)

    for jugador, coord in zip(jugadores, coordenadas):

        jugador.pca_x = float(coord[0])
        jugador.pca_y = float(coord[1])

        jugador.entrenado = True

        jugador.save()

    joblib.dump(pca, MODEL_PATH)

    generar_grafica()

def generar_grafica():

    jugadores = Jugador.objects.filter(
        entrenado=True
    )

    xs = [j.pca_x for j in jugadores]
    ys = [j.pca_y for j in jugadores]

    nombres = [j.nombre for j in jugadores]

    plt.figure(figsize=(10, 8))

    plt.scatter(xs, ys)

    for i, nombre in enumerate(nombres):

        plt.annotate(
            nombre,
            (xs[i], ys[i])
        )

    plt.xlabel("PCA X")
    plt.ylabel("PCA Y")

    plt.title("Jugadores PCA")

    plt.savefig(GRAPH_PATH)

    plt.close()