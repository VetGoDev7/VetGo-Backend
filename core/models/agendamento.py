from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Agendamento(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    )

    data_hora = models.DateTimeField()
    pet = models.ForeignKey('Pet', on_delete=models.PROTECT, related_name='agendamentos')
    veterinario = models.ForeignKey('Veterinario', on_delete=models.PROTECT, related_name='agendamentos')
    servico = models.ForeignKey('Servico', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def clean(self):
        if not self.veterinario:
            raise ValidationError('O veterinário deve ser informado.')
        conflito = Agendamento.objects.filter(
            veterinario=self.veterinario, data_hora=self.data_hora, status__in=['pendente', 'confirmado']
        )
        if self.pk:
            conflito = conflito.exclude(pk=self.pk)
        if conflito.exists():
            raise ValidationError('O veterinário já possui um agendamento nesse horário.')
        if self.data_hora and self.data_hora < timezone.now():
            raise ValidationError('A data e hora do agendamento não pode ser passada.')

    def __str__(self):
        pet_nome = self.pet.nome if self.pet else 'Sem Pet'
        vet_nome = (
            getattr(self.veterinario, 'nome_completo', None) or str(self.veterinario)
            if self.veterinario
            else 'Sem Veterinário'
        )
        return f'Agendamento: {self.data_hora} - {pet_nome} - {vet_nome}'

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['data_hora']
