from rest_framework import serializers
from django.utils import timezone
from datetime import time
from core.models import Agendamento, Pet, Veterinario, Servico


class PetNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'nome', 'especie', 'raca', 'idade']


class AgendamentoSerializer(serializers.ModelSerializer):
    pet_info = PetNestedSerializer(source='pet', read_only=True)

    veterinario_info = serializers.SerializerMethodField()
    servico_info = serializers.SerializerMethodField()

    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all(), write_only=True)
    veterinario = serializers.PrimaryKeyRelatedField(queryset=Veterinario.objects.all(), write_only=True)
    servico = serializers.PrimaryKeyRelatedField(queryset=Servico.objects.all(), write_only=True)

    class Meta:
        model = Agendamento
        fields = [
            'id',
            'data_hora',
            'status',
            'pet',
            'pet_info',
            'veterinario',
            'veterinario_info',
            'servico',
            'servico_info',
            'criado_por',
        ]
        read_only_fields = ['id', 'criado_por', 'pet_info', 'veterinario_info', 'servico_info']

    def get_veterinario_info(self, obj):
        vet = obj.veterinario
        return {
            'id': vet.id,
            'nome_completo': getattr(vet, 'nome_completo', None),
            'especialidade': getattr(vet, 'especialidade', None),
        }

    def get_servico_info(self, obj):
        s = obj.servico
        return {'id': s.id, 'nome': getattr(s, 'nome', None)}

    def validate_data_hora(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('A data e hora do agendamento não pode ser no passado.')

        if value.weekday() > 4:
            raise serializers.ValidationError('Agendamentos só podem ser feitos de segunda a sexta.')

        if not (time(8, 0) <= value.time() <= time(17, 0)):
            raise serializers.ValidationError('Horário permitido: 08:00 às 17:00.')

        return value

    def validate(self, attrs):
        request = self.context.get('request')
        pet = attrs.get('pet')
        veterinario = attrs.get('veterinario')
        data_hora = attrs.get('data_hora')

        if request and hasattr(request.user, 'tutor'):
            tutor = request.user.tutor
            if pet.tutor != tutor:
                raise serializers.ValidationError('Você só pode agendar consultas para seus próprios pets.')

        if veterinario and data_hora:
            conflito = Agendamento.objects.filter(
                veterinario=veterinario, data_hora=data_hora, status__in=['pendente', 'confirmado']
            )
            if self.instance:
                conflito = conflito.exclude(id=self.instance.id)

            if conflito.exists():
                raise serializers.ValidationError('O veterinário já possui um agendamento neste horário.')

        if pet:
            conflito_pet = Agendamento.objects.filter(pet=pet, status__in=['pendente', 'confirmado'])
            if self.instance:
                conflito_pet = conflito_pet.exclude(id=self.instance.id)

            if conflito_pet.exists():
                raise serializers.ValidationError('Este pet já possui um agendamento ativo.')

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['criado_por'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if request and hasattr(request.user, 'tutor'):
            validated_data.pop('status', None)

        return super().update(instance, validated_data)
