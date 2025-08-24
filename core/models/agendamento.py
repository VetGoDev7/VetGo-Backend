from django.db import models
from django.core.exceptions import ValidationError
from core.models import Veterinario, Tutor, Pet, Servico


class Agendamento(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    )

    data_hora = models.DateTimeField()
    tutor = models.ForeignKey(Tutor, on_delete=models.PROTECT, related_name='agendamentos')
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT, related_name='agendamentos')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.PROTECT, related_name='agendamentos')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, related_name='agendamentos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def clean(self):
        if self.pet.tutor != self.tutor:
            raise ValidationError('O pet selecionado não pertence a este tutor.')

        conflito = Agendamento.objects.filter(
            veterinario=self.veterinario, data_hora=self.data_hora, status__in=['pendente', 'confirmado']
        )

        if self.pk:
            conflito = conflito.exclude(pk=self.pk)

        if conflito.exists():
            raise ValidationError('O veterinário já possui um agendamento nesse horário.')

    def __str__(self):
        return f'Agendamento: {self.data_hora} - {self.pet.nome} - {self.veterinario.user.email}'
