from django.db import models

class Jugador(models.Model):

    nombre = models.CharField(max_length=100)

    velocidad = models.FloatField()
    agilidad = models.FloatField()
    fuerza = models.FloatField()
    potencia = models.FloatField()

    edad = models.FloatField()
    peso = models.FloatField()
    altura = models.FloatField()

    partidos_jugados = models.FloatField()
    puntos_anotados = models.FloatField()
    partidos_ganados = models.FloatField()

    entrenado = models.BooleanField(default=False)

    pca_x = models.FloatField(null=True, blank=True)
    pca_y = models.FloatField(null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)

    def vector_pca(self):

        return [
            self.velocidad,
            self.agilidad,
            self.fuerza,
            self.potencia,
            self.edad,
            self.peso,
            self.altura,
            self.partidos_jugados,
            self.puntos_anotados,
            self.partidos_ganados
        ]

    def __str__(self):
        return self.nombre