from rest_framework.viewsets import ModelViewSet

from core.models import Pet
from core.serializers import PetSerializer


class PetViewsets(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
