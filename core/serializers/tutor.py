from rest_framework import serializers
from core.models import Tutor
from django.contrib.auth.hashers import make_password


class TutorSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=True, min_length=8)
    confirmar_senha = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = Tutor
        fields = [
            'id',
            'nome_completo',
            'email',
            'senha',
            'confirmar_senha',
        ]
        read_only_fields = ['id']

    def validate_email(self, value):
        tutor_existente = Tutor.objects.filter(email=value).first()
        if tutor_existente and self.instance != tutor_existente:
            raise serializers.ValidationError('Este email já está cadastrado.')
        return value

    def validate(self, data):
        if data['senha'] != data['confirmar_senha']:
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
