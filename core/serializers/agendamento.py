from rest_framework import serializers
from django.utils import timezone
from datetime import time
from core.models import Agendamento, Pet, Veterinario, Servico

class PetNestedSerializer(serializers.ModelSerializer):
    tutor_info = serializers.SerializerMethodField()
    class Meta:
        model = Pet
        fields = ['id', 'nome', 'especie', 'raca', 'idade', 'tutor_info']

    def get_tutor_info(self, obj):
        tutor = obj.tutor
        if not tutor:
            return None
        return {
            'id': tutor.id,
            'name': getattr(tutor, 'name', '') or '',
            'email': getattr(tutor, 'email', '') or '',
        }
    

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'tutor'):
            self.fields['pet'].queryset = Pet.objects.filter(tutor=request.user.tutor)

    def get_veterinario_info(self, obj):
        vet = obj.veterinario
        if not vet:
            return None
        return {
            'id': vet.id,
            'nome_completo': getattr(vet, 'nome_completo', '') or '',
            'especialidade': getattr(vet, 'especialidade', '') or '',
        }

    def get_servico_info(self, obj):
        s = obj.servico
        if not s:
            return None
        return {'id': s.id, 'nome': getattr(s, 'nome', '') or ''}

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


        if request and hasattr(request.user, 'tutor') and pet:
            tutor = request.user.tutor
            if pet.tutor != tutor:
                raise serializers.ValidationError('Você só pode agendar consultas para seus próprios pets.')

        # Conflito de horário para veterinário
        if veterinario and data_hora:
            conflito_vet = Agendamento.objects.filter(
                veterinario=veterinario,
                data_hora=data_hora,
                status__in=['pendente', 'confirmado']
            )
            if self.instance:
                conflito_vet = conflito_vet.exclude(id=self.instance.id)
            if conflito_vet.exists():
                raise serializers.ValidationError('O veterinário já possui um agendamento neste horário.')


        if pet and data_hora:
            conflito_pet = Agendamento.objects.filter(
                pet=pet,
                data_hora__gte=timezone.now(),
                status__in=['pendente', 'confirmado']
            )
            if self.instance:
                conflito_pet = conflito_pet.exclude(id=self.instance.id)
            if conflito_pet.exists():
                raise serializers.ValidationError('Este pet já possui um agendamento ativo neste horário.')

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
            validated_data.pop('veterinario', None)
            validated_data.pop('pet', None)
        return super().update(instance, validated_data)
