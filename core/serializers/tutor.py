from rest_framework.serializers import ModelSerializer
from core.models import Tutor


class TutorSerializer(ModelSerializer):
    class Meta:
        model = Tutor
        field = '__all__'
