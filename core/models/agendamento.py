from django.db import models
from django.core.exceptions import ValidationError

class Agendamento(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    )

    data_hora = models.DateTimeField()
    tutor = models.ForeignKey("core.Tutor", on_delete=models.PROTECT, related_name='agendamentos')
    pet = models.ForeignKey("core.Pet", on_delete=models.PROTECT, related_name='agendamentos')
    veterinario = models.ForeignKey("core.Veterinario", on_delete=models.PROTECT, related_name='agendamentos')
    servico = models.ForeignKey("core.Servico", on_delete=models.PROTECT, related_name='agendamentos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def clean(self):
        # Validação para garantir que o pet pertence ao tutor
        if self.pet and self.tutor and self.pet.tutor_id != self.tutor.id:
            raise ValidationError('O pet selecionado não pertence a este tutor.')

        # Verificação de conflitos de agendamento
        conflito = Agendamento.objects.filter(
            veterinario=self.veterinario,
            data_hora=self.data_hora,
            status__in=['pendente', 'confirmado']
        )
        if self.pk:
            conflito = conflito.exclude(pk=self.pk)

        if conflito.exists():
            raise ValidationError('O veterinário já possui um agendamento nesse horário.')

    def __str__(self):
        return f'Agendamento: {self.data_hora} - {self.pet.nome} - {self.veterinario.user.email}'

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['data_hora']
