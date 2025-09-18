from rest_framework.viewsets import ModelViewSet

from core.models import Servico
from core.serializers import ServicoSerializer


class ServicoViewSet(ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome']
