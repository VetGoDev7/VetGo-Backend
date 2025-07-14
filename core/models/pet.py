from django.db import models

class Pet (models.Model):
    nome = models.CharField(max_length=45)
    especie = models.CharField(max_length=45)
    raca = models.CharField(max_length=45)
    obsevarçao = models.CharField(max_length=255)


    def __str__(self):
        return f'({self.id}) {self.nome} ({self.raca}) ({self.especie}) ({self.obsevarçao})'