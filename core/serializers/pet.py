from rest_framework import serializers
from core.models import Pet


class PetSerializer(serializers.ModelSerializer):
    tutor_info = serializers.SerializerMethodField()
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
            'tutor_info',
        ]
        extra_kwargs = {'tutor': {'write_only': True}}
    def get_tutor_info(self, obj):
        tutor = obj.tutor
        if not tutor:
            return None
        return {
            'id': tutor.id,
            'name': getattr(tutor, 'name', '') or '',
            'email': getattr(tutor, 'email', '') or '',
        }