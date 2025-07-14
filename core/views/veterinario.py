from rest_framework.viewsets import ModelViewSet

from core.models import Veterinario
from core.serializers import VeterinarioSerializer


class VeterinarioViewsets(ModelViewSet):
    queryset = Veterinario.objects.all()
    serializer_class = VeterinarioSerializer
