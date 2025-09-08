from rest_framework import serializers
from core.models import Tutor


class TutorSerializer(serializers.ModelSerializer):
    # Campos computados/adicionais (opcional)
    qtd_pets = serializers.SerializerMethodField()
    telefone_formatado = serializers.SerializerMethodField()

    class Meta:
        model = Tutor
        fields = [
            'id',
            'nome_completo',
            'email',
            'telefone',
            'telefone_formatado',
            'endereco',
            'qtd_pets',
            #'created_at',
            #'updated_at',
        ]
        read_only_fields = ['id']
        extra_kwargs = {'email': {'required': True}, 'nome_completo': {'required': True}}

    def get_qtd_pets(self, obj):
        """Retorna a quantidade de pets do tutor"""
        return obj.pets.count() if hasattr(obj, 'pets') else 0

    def get_telefone_formatado(self, obj):
        """Formata o telefone para exibição (##) #####-####"""
        if not obj.telefone:
            return ''

        telefone = obj.telefone
        if len(telefone) == 11:
            return f'({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}'
        elif len(telefone) == 10:
            return f'({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}'
        return telefone

    def validate_email(self, value):
        """Validação customizada para email"""
        if Tutor.objects.filter(email=value).exists():
            if self.instance and self.instance.email == value:
                return value
            raise serializers.ValidationError('Este email já está cadastrado.')
        return value

    def validate_telefone(self, value):
        """Validação customizada para telefone"""
        if value and not value.isdigit():
            raise serializers.ValidationError('O telefone deve conter apenas números.')
        return value
