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
            'observacao',
            'tutor',
            'tutor_nome',
            'tutor_email',
        ]
        read_only_fields = ['id', 'idade']
        extra_kwargs = {'tutor': {'write_only': True}}
