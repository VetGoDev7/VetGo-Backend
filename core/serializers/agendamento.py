from rest_framework.serializers import ModelSerializer


from core.models import Agendamento


class AgendamentoSealizer(ModelSerializer):
    class Meta:
        model = Agendamento
        field = '__all_'
