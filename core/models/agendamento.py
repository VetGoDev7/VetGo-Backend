from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings


class Agendamento(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    )

    data_hora = models.DateTimeField()
    pet = models.ForeignKey('core.Pet', on_delete=models.PROTECT, related_name='agendamentos')
    veterinario = models.ForeignKey('core.Veterinario', on_delete=models.PROTECT, related_name='agendamentos')
    servico = models.ForeignKey('core.Servico', on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        if not self.veterinario:
            raise ValidationError('O veterinário deve ser informado.')

        if self.data_hora and self.data_hora < timezone.now():
            raise ValidationError('A data e hora do agendamento não pode ser passada.')

        if self.data_hora:
            weekday = self.data_hora.weekday()
            if weekday > 4:
                raise ValidationError('Agendamentos só podem ser feitos de segunda a sexta-feira.')

            start = self.data_hora.replace(hour=8, minute=0, second=0, microsecond=0).time()
            end = self.data_hora.replace(hour=17, minute=0, second=0, microsecond=0).time()
            if not (start <= self.data_hora.time() <= end):
                raise ValidationError('Horário permitido para agendamento: das 08:00 às 17:00.')

        conflito = Agendamento.objects.filter(
            veterinario=self.veterinario,
            data_hora=self.data_hora,
            status__in=['pendente', 'confirmado']
        )
        if self.pk:
            conflito = conflito.exclude(pk=self.pk)
        if conflito.exists():
            raise ValidationError('O veterinário já possui um agendamento nesse horário.')

        if self.pet:
            existe = Agendamento.objects.filter(
                pet=self.pet,
                status__in=['pendente', 'confirmado']
            )
            if self.pk:
                existe = existe.exclude(pk=self.pk)
            if existe.exists():
                raise ValidationError('Este pet já possui um agendamento ativo.')

    def __str__(self):
        pet_nome = getattr(self.pet, 'nome', 'Sem Pet')
        vet_nome = getattr(self.veterinario, 'nome_completo', str(self.veterinario) if self.veterinario else 'Sem Veterinário')
        return f'Agendamento: {self.data_hora} - {pet_nome} - {vet_nome}'

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['data_hora']