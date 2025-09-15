from django.db import models
from django.core.exceptions import ValidationError
from core.models import Tutor


class Pet(models.Model):
    STATUS_CHOICES = (
        ('cachorro', 'Cachorro'),
        ('gato', 'Gato'),
    )
    nome = models.CharField(max_length=45)
    especie = models.CharField(max_length=20, choices=STATUS_CHOICES)
    raca = models.CharField(max_length=45, blank=True, null=True)
    idade = models.PositiveIntegerField(blank=True, null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        if not self.tutor:
            raise ValidationError('O pet deve ter um tutor associado.')

        if self.peso and self.peso <= 0:
            raise ValidationError('O peso deve ser maior que zero.')

    def __str__(self):
        tutor_nome = self.tutor.nome_completo if self.tutor else 'Sem tutor'
        return f'{self.nome} ({self.raca}) - {self.especie} | Tutor: {tutor_nome}'

    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        ordering = ['nome']
