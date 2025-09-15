from rest_framework import serializers
from core.models import Tutor


class TutorSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=True)
    confirmar_senha = serializers.CharField(write_only=True, required=True)
    qtd_pets = serializers.SerializerMethodField()

    class Meta:
        model = Tutor
        fields = [
            'id',
            'nome_completo',
            'email',
            'senha',
            'confirmar_senha',
            'qtd_pets',
            # 'created_at',
            # 'updated_at',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'required': True},
            'nome_completo': {'required': True},
        }

    def get_qtd_pets(self, obj):
        return obj.pets.count() if hasattr(obj, 'pets') else 0

    def validate_email(self, value):
        if Tutor.objects.filter(email=value).exists():
            if self.instance and self.instance.email == value:
                return value
            raise serializers.ValidationError('Este email já está cadastrado.')
        return value


def create(self, validated_data):
    validated_data.pop('confirmar_senha')
    validated_data['senha'] = 'make_password'(validated_data['senha'])
    return super().create(validated_data)


def update(self, instance, validated_data):
    validated_data.pop('confirmar_senha', None)
    if 'senha' in validated_data:
        validated_data['senha'] = 'make_password'(validated_data['senha'])
    return super().update(instance, validated_data)
