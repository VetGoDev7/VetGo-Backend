from rest_framework.viewsets import ModelViewSet

from core.models import Servico
from core.serializers import ServicoSerializer


class ServicoViewsets(ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
