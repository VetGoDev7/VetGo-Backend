from rest_framework.serializers import ModelSerializer
from core.models import Servico


class ServicoSerializer(ModelSerializer):
    class Meta:
        model = Servico
        field = '__all__'
