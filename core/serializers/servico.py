from rest_framework import serializers
from core.models import Servico


class ServicoSerializer(serializers.ModelSerializer):
    qtd_agendamentos = serializers.SerializerMethodField()

    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'qtd_agendamentos', ]
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
        return obj.agendamentos.count() if hasattr(obj, 'agendamentos') else 0

    def validate_nome(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError('O nome do serviço deve ter pelo menos 2 caracteres.')

        queryset = Servico.objects.filter(nome__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError('Já existe um serviço com este nome.')

        return value

    def validate_descricao(self, value):
        if value and len(value.strip()) < 10:
            raise serializers.ValidationError('A descrição deve ter pelo menos 10 caracteres.')
        return value.strip() if value else value

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['nome_formatado'] = instance.nome.title()

        return representation
