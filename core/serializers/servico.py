from rest_framework import serializers
from core.models import Servico


class ServicoSerializer(serializers.ModelSerializer):
    qtd_agendamentos = serializers.SerializerMethodField()

    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'qtd_agendamentos']
        read_only_fields = ['id', 'qtd_agendamentos']
        extra_kwargs = {
            'nome': {
                'required': True,
                'error_messages': {
                    'required': 'O nome do serviço é obrigatório.',
                    'blank': 'O nome do serviço não pode estar em branco.',
                },
            },
            'descricao': {'required': False, 'allow_blank': True},
        }

    def get_qtd_agendamentos(self, obj):
        try:
            if hasattr(obj, 'agendamentos'):
                return obj.agendamentos.count()
            if hasattr(obj, 'agendamento_set'):
                return obj.agendamento_set.count()
        except Exception:
            return 0
        return 0
