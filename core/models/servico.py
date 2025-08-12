from django.db import models


class Servico(models.Model):
    nome = models.CharField(max_length=45)
    descricao = models.CharField(max_length=255)
    tutor = models.ForeignKey('core.Tutor', on_delete=models.PROTECT, related_name='servicos', null=True, blank=True)

    def __str__(self):
        return f'({self.id}) {self.nome} ({self.descricao})'
