from rest_framework import serializers
from core.models import Tutor


class TutorSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=True)
    confirmar_senha = serializers.CharField(write_only=True, required=True)
    qtd_pets = serializers.SerializerMethodField()

    class Meta:
        model = Tutor
        fields = ['id', 'nome_completo', 'email', 'senha', 'confirmar_senha', 'qtd_pets']
        read_only_fields = ['id']
        extra_kwargs = {'email': {'required': True}, 'nome_completo': {'required': True}}

    def get_qtd_pets(self, obj):
        return obj.pets.count() if hasattr(obj, 'pets') else 0

    def validate(self, data):
        if data['senha'] != data['confirmar_senha']:
            raise serializers.ValidationError({"confirmar_senha": "As senhas não coincidem."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirmar_senha')
        senha = validated_data.pop('senha')
        tutor = Tutor(**validated_data)
        tutor.set_password(senha)
        tutor.save()
        return tutor

    def update(self, instance, validated_data):
        validated_data.pop('confirmar_senha', None)
        senha = validated_data.pop('senha', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if senha:
            instance.set_password(senha)
        instance.save()
        return instance
