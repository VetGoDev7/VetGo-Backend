
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from core.models import Pet
from core.serializers import PetSerializer


class IsAdminOrTutorPet(permissions.BasePermission):


    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff:
            return True

        if hasattr(user, 'tutor'):
            return obj.tutor == user.tutor

        return False


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAdminOrTutorPet]

    def get_queryset(self):
        user = self.request.user


        if user.is_staff:
            return Pet.objects.all().order_by('nome')


        if hasattr(user, 'tutor'):
            return Pet.objects.filter(tutor=user.tutor).order_by('nome')


        return Pet.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user

        if hasattr(user, 'tutor'):
            serializer.save(tutor=user.tutor)
        else:
            serializer.save()


    def perform_update(self, serializer):
        user = self.request.user

        if hasattr(user, 'tutor'):
            if "tutor" in serializer.validated_data:
                raise PermissionDenied("Você não pode alterar o tutor deste pet.")

            serializer.save()
        else:
            serializer.save()
