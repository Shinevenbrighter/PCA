from django.db import models

# Create your models here.

class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.FloatField()
    altura = models.FloatField()
    peso = models.FloatField()
    velocidad = models.FloatField()
    agilidad = models.FloatField()
    fuerza = models.FloatField()
    potencia  = models.FloatField()
    partidos_jugados = models.FloatField()
    puntos_anotados = models.FloatField()
    partidos_ganados = models.FloatField()

    entrenado = models.BooleanField(default=False)

    pca_x = models.FloatField(null=True, blank=True)
    pca_y = models.FloatField(null=True, blank=True)



def valores_pca(self):
    return[
        self.edad,
        self.altura,
        self.peso,
        self.velocidad,
        self.agilidad,
        self.fuerza,
        self.potencia,
        self.partidos_jugados,
        self.puntos_anotados,
        self.partidos_ganados,
    ]

def __str__(self):
        return self.nombre
