from django.db import models


class Veterinario(models.Model):
    espectalidade = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    horario_atedimento = models.DateTimeField()


def __str__(self):
    return f'({self.id}) {self.email} ({self.horario_atedimento})'
