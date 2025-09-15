from rest_framework.viewsets import ModelViewSet
from core.models import Veterinario
from core.serializers import VeterinarioSerializer


class VeterinarioViewSet(ModelViewSet):
<<<<<<< HEAD
    queryset = Veterinario.objects.all()
=======

    queryset = Veterinario.objects.all() 
>>>>>>> 0f87b8cf1c4042b1a43f1158da62e4492b30cdee
    serializer_class = VeterinarioSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
<<<<<<< HEAD
        instance.delete()
=======

        instance.delete() 
>>>>>>> 0f87b8cf1c4042b1a43f1158da62e4492b30cdee
