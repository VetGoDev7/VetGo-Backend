from rest_framework.viewsets import ModelViewSet
from core.models import Veterinario
from core.serializers import VeterinarioSerializer


class VeterinarioViewSet(ModelViewSet):
    queryset = Veterinario.objects.all()
    serializer_class = VeterinarioSerializer

    def perform_create(self, serializer):

        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):

        instance.delete()
