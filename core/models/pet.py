from django.db import models
from django.core.exceptions import ValidationError
from core.models.user import User
  

class Pet(models.Model):
    ESPECIE_CHOICES = [
        ('cachorro', 'Cachorro'),
        ('gato', 'Gato'),
    ]

    nome = models.CharField(max_length=45)
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    raca = models.CharField(max_length=45, blank=True, null=True)
    idade = models.PositiveIntegerField(blank=True, null=True)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    tutor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="pets")

    def clean(self):
        if not self.tutor:
            raise ValidationError('O pet deve ter um tutor associado.')

    def __str__(self):
        tutor_nome = self.tutor.name if self.tutor else 'Sem tutor'
        return f'{self.nome} ({self.raca or "Sem raça"}) - {self.especie} | Tutor: {tutor_nome}'

    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        ordering = ['nome']
