from django.db import models


class Pet(models.Model):
    nome = models.CharField(max_length=45)
    especie = models.CharField(max_length=45)
    raca = models.CharField(max_length=45)
    observacao = models.CharField(max_length=255)
    tutor = models.ForeignKey('core.Tutor', on_delete=models.PROTECT, related_name='pets', null=True, blank=True)

    def __str__(self):
        return f'({self.id}) {self.nome} ({self.raca}) ({self.especie}) ({self.observacao})'
