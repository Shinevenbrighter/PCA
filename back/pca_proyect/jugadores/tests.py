import os 
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Jugador
from .services import verificar_modelo

# Datos reutilizables en todos los tests que necesiten un jugador válido
DATOS_JUGADOR ={
    "nombre": "Test Player",
    "velocidad": 85.0,
    "agilidad": 78.5,
    "fuerza": 90.0,
    "potencia": 88.0,
    "edad": 25.0,
    "peso": 75.0,
    "altura": 1.80,
    "partidos_jugados": 30.0,
    "puntos_anotados": 150.0,
    "partidos_ganados": 20.0,
}


class CrearJugadorTests(APITestCase):

    def setUp(self):
        # URL del endpoint y datos base disponibles para el test de la clase
        self.url = '/api/jugadores/'

# TEST 1: verifica que el endpoint (POST /api/jugadores/) retorna 400 cuando falta el campo nombre
    def test_sin_nombre_retorna_400(self):
        # se quita el campo nombre y verificamos que el serializador lo rechace
        datos = {**DATOS_JUGADOR} # se genera una copia de los datos base 
        datos.pop('nombre') # se elimina campo nombre 

        response = self.client.post(self.url, datos, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nombre', response.data) # se verifica que el error corresponda al campo nombre

# TEST 2: verifica que el endpoint (POST /api/jugadores/) con body vacio debe retornar 400
    def test_body_vacio_retorna_400(self):
        response = self.client.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 



class ObtenerGraficaTests(APITestCase):

    def setUp(self):
        self.url = '/api/grafica/'
        self.path_grafica = os.path.join(settings.BASE_DIR, 'static', 'pca_actual.png')

    def tearDown(self):
        # limpia el archivo después de cada test sin importar qué pasó
        if os.path.exists(self.path_grafica):
            os.remove(self.path_grafica)

    def test_grafica_no_existe_retorna_404(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_grafica_existe_retorna_200(self):
        os.makedirs(os.path.dirname(self.path_grafica), exist_ok=True)
        with open(self.path_grafica, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'image/png')
        # ya no borras aquí, lo hace tearDown

class VectorPCATests(APITestCase):

    def setUp(self):
        self.jugador = Jugador.objects.create(**DATOS_JUGADOR) # se crea un jugador con los datos base para probar el método vector_pca

# TEST 5: vector_pca() debe retornar una lista con exactamente 10 valores
    def test_vector_pca_retorna_10_valores(self):
        vector = self.jugador.vector_pca() # se llama directamente a la función del modelo

        self.assertEqual(len(vector), 10) # se verifica que el vector tenga 10 elementos 

# TEST 6:  vector_pca() debe retornar los valores en el orden correcto
    def test_vector_pca_valores_correctos(self):
        vector = self.jugador.vector_pca() # se llama directamente a la función del modelo

        self.assertEqual(vector[0], 85.0)   # velocidad
        self.assertEqual(vector[1], 78.5)   # agilidad
        self.assertEqual(vector[2], 90.0)   # fuerza
        self.assertEqual(vector[3], 88.0)   # potencia
        self.assertEqual(vector[4], 25.0)   # edad
        self.assertEqual(vector[5], 75.0)   # peso
        self.assertEqual(vector[6], 1.80)   # altura
        self.assertEqual(vector[7], 30.0)   # partidos_jugados
        self.assertEqual(vector[8], 150.0)  # puntos_anotados
        self.assertEqual(vector[9], 20.0)   # partidos_ganados



class VerificarModeloTests(APITestCase):

    def setUp(self):
        self.datos = DATOS_JUGADOR

# TEST 7: verificar_modelo() no debe entrenar si hay menos de 20 jugadores pendientes
    def test_no_entrena_con_menos_de_20_jugadores(self):
       Jugador.objects.create(**self.datos) # se crea solo un jugador
       verificar_modelo() # se llama directamente a la función
       
       self.assertFalse(Jugador.objects.first().entrenado) # verifica que el jugador no fue entrenado 

# TEST 8: verificar_modelo() debe entrenar si hay exactamente 20 jugadores pendientes
    def test_entrena_con_20_jugadores(self):
        for i in range(20):
            Jugador.objects.create(**{**self.datos, 'nombre': f'Jugador {i}'}) # se crean 20 jugadores con nombres únicos

        verificar_modelo() # se llama directamente a la función
        entrenados = Jugador.objects.filter(entrenado=True).count() # se cuenta cuántos jugadores fueron entrenados
        self.assertEqual(entrenados,20) # se verifica que los 20 jugadores fueron entrenados.