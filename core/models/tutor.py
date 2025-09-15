from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import make_password


class Tutor(models.Model):
    nome_completo = models.CharField(max_length=45, verbose_name='Nome Completo')
    email = models.EmailField(
        max_length=45,
        unique=True,
        validators=[EmailValidator()],
        verbose_name='E-mail'
    )
    senha = models.CharField(max_length=128, verbose_name='Senha', null=True, blank=True)

    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"

    def __str__(self):
        return self.nome_completo

    def set_password(self, raw_password):

        self.senha = make_password(raw_password)
