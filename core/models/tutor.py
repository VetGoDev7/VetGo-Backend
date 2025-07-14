from django.db import models


class Tutor(models.Model):
    nome_completo = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    telefone = models.CharField(max_length=11)
    endereco = models.CharField(max_length=60)


def __str__(self):
    return f'({self.id}) {self.nome} ({self.email})'
