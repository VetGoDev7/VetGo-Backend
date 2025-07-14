from rest_framework.serializers import ModelSerializer
from core.models import Pet


class PetSerializer(ModelSerializer):
    class Meta:
        model = Pet
        field = '__all__'
