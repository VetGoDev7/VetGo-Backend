from django.db import models


class Agendamento(models.Model):
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=45)


def __str__(self):
    return f'({self.id}) {self.data_hora} ({self.status})'
