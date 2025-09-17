from rest_framework import serializers
from core.models import Tutor
from django.contrib.auth.hashers import make_password

class TutorSerializer(serializers.ModelSerializer):
    qtd_pets = serializers.SerializerMethodField()

    senha = serializers.CharField(write_only=True, required=True, min_length=8)
    confirmar_senha = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = Tutor
        fields = [
            'id',
            'nome_completo',
            'email',
            'qtd_pets',
            'senha',
            'confirmar_senha',
        ]
        read_only_fields = ['id']
        extra_kwargs = {'email': {'required': True}, 'nome_completo': {'required': True}}

    def get_qtd_pets(self, obj):
        return obj.pets.count() if hasattr(obj, 'pets') else 0

    def validate_email(self, value):
        if Tutor.objects.filter(email=value).exists():
            if self.instance and self.instance.email == value:
                return value
            raise serializers.ValidationError('Este email já está cadastrado.')
        return value

    def validate(self, data):
        senha = data.get('senha')
        confirmar_senha = data.get('confirmar_senha')
        if senha != confirmar_senha:
            raise serializers.ValidationError({'confirmar_senha': 'As senhas não coincidem.'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirmar_senha')
        senha = validated_data.pop('senha')
        validated_data['senha'] = make_password(senha)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('confirmar_senha', None)
        senha = validated_data.pop('senha', None)
        if senha:
            instance.senha = make_password(senha)
        return super().update(instance, validated_data)
