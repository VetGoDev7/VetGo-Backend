from rest_framework import serializers
from django.utils import timezone
from core.models import Agendamento
from core.serializers import TutorSerializer, PetSerializer, VeterinarioSerializer, ServicoSerializer


class AgendamentoSerializer(serializers.ModelSerializer):
    tutor_info = TutorSerializer(source='tutor', read_only=True)
    pet_info = PetSerializer(source='pet', read_only=True)
    veterinario_info = VeterinarioSerializer(source='veterinario', read_only=True)
    servico_info = ServicoSerializer(source='servico', read_only=True)

    class Meta:
        model = Agendamento
        fields = [
            'id',
            'data_hora',
            'status',
            'tutor',
            'tutor_info',
            'pet',
            'pet_info',
            'veterinario',
            'veterinario_info',
            'servico',
            'servico_info',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'tutor': {'write_only': True},
            'pet': {'write_only': True},
            'veterinario': {'write_only': True},
            'servico': {'write_only': True},
        }

    def validate(self, data):
        if data.get('pet') and data.get('tutor'):
            if data['pet'].tutor != data['tutor']:
                raise serializers.ValidationError('O pet selecionado não pertence a este tutor.')

        if not data.get('veterinario'):
            raise serializers.ValidationError('O veterinário deve ser informado.')

        return data

    def validate_data_hora(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('A data e hora do agendamento não pode ser passada.')
        return value
