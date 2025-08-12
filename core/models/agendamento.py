from django.db import models
from core.models import Veterinario, Tutor

class Agendamento(models.Model):
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=45)
    tutor = models.ForeignKey(Tutor, on_delete=models.PROTECT, related_name='tutor', null=True, blank=True)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.PROTECT, related_name='veterinario', null=True, blank=True)

    def __str__(self):
        return f'({self.id}) {self.data_hora} ({self.status})'
