from rest_framework import serializers
from core.models import Pet


class PetSerializer(serializers.ModelSerializer):
    idade = serializers.IntegerField(read_only=True)
    tutor_nome = serializers.CharField(source='tutor.nome_completo', read_only=True)
    tutor_email = serializers.CharField(source='tutor.email', read_only=True)

    class Meta:
        model = Pet
        fields = [
            'id',
            'nome',
            'especie',
            'raca',
            'idade',
            'peso',
            'observacao',
            'tutor',
            'tutor_nome',
            'tutor_email',
            #'data_cadastro',
            #'data_atualizacao',
        ]
        read_only_fields = ['id', 'idade']
        extra_kwargs = {'tutor': {'write_only': True}}

    def validate_peso(self, value):
        if value and value <= 0:
            raise serializers.ValidationError('O peso deve ser maior que zero.')
        return value

    def validate(self, data):
        if data.get('peso') and data.get('especie') == 'ave' and data['peso'] > 10:
            raise serializers.ValidationError('Peso muito alto para uma ave.')
        return data
