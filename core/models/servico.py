from django.db import models
from core.models.user import User

class Servico(models.Model):
    nome = models.CharField(max_length=45)
    descricao = models.CharField(max_length=255)
    tutor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='servicos', null=True, blank=True)

    def __str__(self):
        tutor_nome = self.tutor.name if self.tutor else 'Sem tutor'
        return f'{self.nome} - {self.descricao} | Tutor: {tutor_nome}'
