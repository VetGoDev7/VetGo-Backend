from rest_framework import serializers
from core.models import Veterinario


class VeterinarioSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    qtd_agendamentos = serializers.SerializerMethodField()
    horario_atendimento_formatado = serializers.SerializerMethodField()

    class Meta:
        model = Veterinario
        fields = [
            'id',
            'nome_completo',
            'email',
            'especialidade',
            'horario_atendimento',
            'horario_atendimento_formatado',
            'crmv',
            'telefone',
            'qtd_agendamentos',
            #'created_at',
            #'updated_at',
        ]
        read_only_fields = ['id', 'qtd_agendamentos']
        extra_kwargs = {
            'especialidade': {'required': True},
            'crmv': {'required': True},
            'horario_atendimento': {'required': True},
        }

    def get_qtd_agendamentos(self, obj):
        return obj.agendamentos.count() if hasattr(obj, 'agendamentos') else 0

    def get_horario_atendimento_formatado(self, obj):
        if not obj.horario_atendimento:
            return ''

        return obj.horario_atendimento

    def validate_crmv(self, value):
        if not value:
            raise serializers.ValidationError('O CRMV é obrigatório.')

        crmv_clean = ''.join(filter(str.isdigit, value))

        if len(crmv_clean) < 5:
            raise serializers.ValidationError('O CRMV deve ter pelo menos 5 dígitos.')

        queryset = Veterinario.objects.filter(crmv=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError('Já existe um veterinário com este CRMV.')

        return value

    def validate_especialidade(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError('A especialidade deve ter pelo menos 3 caracteres.')
        return value

    def validate_horario_atendimento(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError('O horário de atendimento é obrigatório.')
        return value.strip()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if 'especialidade' in representation and representation['especialidade']:
            representation['especialidade'] = representation['especialidade'].title()

        return representation
