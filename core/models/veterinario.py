from django.db import models
from django.core.validators import EmailValidator

class Veterinario(models.Model):
    ESPECIALIDADE_CHOICES = [
        ('clinica_geral', 'Clínica Geral'),
        ('cirurgia', 'Cirurgia'),
        ('odontologia', 'Odontologia'),
        ('dermatologia', 'Dermatologia'),
        ('oftalmologia', 'Oftalmologia'),
        ('cardiologia', 'Cardiologia'),
    ]
    
    nome_completo = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=45, choices=ESPECIALIDADE_CHOICES)
    email = models.EmailField(validators=[EmailValidator()])
    telefone = models.CharField(max_length=11)
    horario_atendimento = models.CharField(max_length=100)
    crmv = models.CharField(max_length=10, unique=True, verbose_name='CRMV')

    def __str__(self):
        return f'{self.nome_completo} - {self.get_especialidade_display()}'

    class Meta:
        verbose_name = 'Veterinário'
        verbose_name_plural = 'Veterinários'
        ordering = ['nome_completo']
