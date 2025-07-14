from rest_framework.serializers import ModelSerializer
from core.models import Veterinario


class VeterinarioSerializer(ModelSerializer):
    class Meta:
        model = Veterinario
        field = '__all__'
