from django.db import models
from django.core.validators import EmailValidator

class Tutor(models.Model):
    nome_completo = models.CharField(
        max_length=45,
        verbose_name='Nome Completo'
    )
    email = models.EmailField(
        max_length=45,
        unique=True,
        validators=[EmailValidator()],
        verbose_name='E-mail'
    )
    telefone = models.CharField(
        max_length=11,
        verbose_name='Telefone'
    )
    endereco = models.CharField(
        max_length=60,
        verbose_name='Endereço'
    )

    def __str__(self):
        return f'{self.nome_completo} - {self.email}'

    class Meta:
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutores'
        ordering = ['nome_completo']
