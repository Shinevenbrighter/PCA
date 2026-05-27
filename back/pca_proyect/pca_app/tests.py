from unittest.mock import patch, MagicMock

import numpy as np
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Jugador


JUGADOR_BASE = {
    "nombre": "Test Player",
    "edad": 25.0,
    "altura": 1.80,
    "peso": 75.0,
    "velocidad": 8.5,
    "agilidad": 7.0,
    "fuerza": 6.5,
    "potencia": 7.5,
    "partidos_jugados": 30.0,
    "puntos_anotados": 150.0,
    "partidos_ganados": 20.0,
}


class PuntosPCATest(TestCase):
    """Tests para GET /api/pca-points/"""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/pca-points/"

    def test_lista_vacia_sin_jugadores_entrenados(self):
        Jugador.objects.create(**JUGADOR_BASE, entrenado=False)
        response = self.client.get(self.url)
        print(f"\n[test_lista_vacia] status={response.status_code} data={response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_retorna_solo_jugadores_entrenados(self):
        entrenado = Jugador.objects.create(
            **JUGADOR_BASE, entrenado=True, pca_x=1.23, pca_y=4.56
        )
        Jugador.objects.create(**{**JUGADOR_BASE, "nombre": "No entrenado"}, entrenado=False)

        response = self.client.get(self.url)
        print(f"\n[test_solo_entrenados] status={response.status_code} data={response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], entrenado.id)
        self.assertEqual(response.data[0]["nombre"], entrenado.nombre)
        self.assertAlmostEqual(response.data[0]["pca_x"], 1.23)
        self.assertAlmostEqual(response.data[0]["pca_y"], 4.56)

    def test_retorna_multiples_jugadores_entrenados(self):
        for i in range(3):
            Jugador.objects.create(
                **{**JUGADOR_BASE, "nombre": f"Jugador {i}"},
                entrenado=True,
                pca_x=float(i),
                pca_y=float(i) * 2,
            )

        response = self.client.get(self.url)
        print(f"\n[test_multiples_jugadores] status={response.status_code} data={response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_campos_en_respuesta(self):
        Jugador.objects.create(**JUGADOR_BASE, entrenado=True, pca_x=0.1, pca_y=0.2)
        response = self.client.get(self.url)
        print(f"\n[test_campos_respuesta] status={response.status_code} keys={set(response.data[0].keys())}")

        keys = set(response.data[0].keys())
        self.assertEqual(keys, {"id", "nombre", "pca_x", "pca_y"})


class ObtenerCoordenadasTest(TestCase):
    """Tests para POST /api/coordenadas/"""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/coordenadas/"
        self.payload = {
            "velocidad": 8.5,
            "agilidad": 7.0,
            "fuerza": 6.5,
            "potencia": 7.5,
            "edad": 25.0,
            "peso": 75.0,
            "altura": 1.80,
            "partidos_jugados": 30.0,
            "puntos_anotados": 150.0,
            "partidos_ganados": 20.0,
        }

    def test_faltan_datos_retorna_400(self):
        payload_incompleto = {"velocidad": 8.5, "agilidad": 7.0}
        response = self.client.post(self.url, payload_incompleto, format="json")
        print(f"\n[test_faltan_datos] status={response.status_code} data={response.data}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_payload_vacio_retorna_400(self):
        response = self.client.post(self.url, {}, format="json")
        print(f"\n[test_payload_vacio] status={response.status_code} data={response.data}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    @patch("pca_app.views.os.path.exists", return_value=False)
    def test_modelo_no_entrenado_retorna_400(self, _mock_exists):
        response = self.client.post(self.url, self.payload, format="json")
        print(f"\n[test_modelo_no_entrenado] status={response.status_code} data={response.data}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    @patch("pca_app.views.os.path.exists", return_value=True)
    @patch("pca_app.views.joblib.load")
    def test_coordenadas_retornadas_correctamente(self, mock_load, _mock_exists):
        mock_pca = MagicMock()
        mock_pca.transform.return_value = np.array([[1.11, 2.22]])
        mock_load.return_value = mock_pca

        response = self.client.post(self.url, self.payload, format="json")
        print(f"\n[test_coordenadas_correctas] status={response.status_code} data={response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data["pca_x"], 1.11)
        self.assertAlmostEqual(response.data["pca_y"], 2.22)

    @patch("pca_app.views.os.path.exists", return_value=True)
    @patch("pca_app.views.joblib.load")
    def test_pca_recibe_datos_en_orden_correcto(self, mock_load, _mock_exists):
        mock_pca = MagicMock()
        mock_pca.transform.return_value = np.array([[0.0, 0.0]])
        mock_load.return_value = mock_pca

        response = self.client.post(self.url, self.payload, format="json")
        print(f"\n[test_orden_datos_pca] status={response.status_code} data={response.data}")

        args, _ = mock_pca.transform.call_args
        entrada = args[0][0]
        expected = [
            self.payload["velocidad"],
            self.payload["agilidad"],
            self.payload["fuerza"],
            self.payload["potencia"],
            self.payload["edad"],
            self.payload["peso"],
            self.payload["altura"],
            self.payload["partidos_jugados"],
            self.payload["puntos_anotados"],
            self.payload["partidos_ganados"],
        ]
        for real, esperado in zip(entrada, expected):
            self.assertAlmostEqual(float(real), esperado)
