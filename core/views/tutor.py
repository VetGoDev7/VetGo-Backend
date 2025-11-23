from rest_framework.permissions import AllowAny
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from core.models import Tutor
from core.serializers import TutorSerializer


class IsAdminOrTheTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff:
            return True

        if hasattr(user, 'tutor'):
            return obj == user.tutor

        return False


class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = [IsAdminOrTheTutor]
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Tutor.objects.all()

        if hasattr(user, 'tutor'):
            return Tutor.objects.filter(id=user.tutor.id)

        return Tutor.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_staff:
            raise PermissionDenied('Apenas admin pode criar tutores.')

        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user

        if hasattr(user, 'tutor'):
            if 'user' in serializer.validated_data:
                raise PermissionDenied('Você não pode alterar o usuário vinculado.')
            if serializer.instance != user.tutor:
                raise PermissionDenied('Você só pode editar seu próprio perfil.')

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if not user.is_staff:
            raise PermissionDenied('Apenas admin pode excluir tutores.')

        instance.delete()
