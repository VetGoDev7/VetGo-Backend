from rest_framework.viewsets import ModelViewSet
from core.models import Servico
from core.serializers import ServicoSerializer
import logging

logger = logging.getLogger(__name__)


class ServicoViewSet(ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome']

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.exception('Erro ao listar serviços: %s', e)
            raise
