from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from core.models import Agendamento
from core.serializers.agendamento import AgendamentoSerializer


class IsAdminOrTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff:
            return True

        if user.tipo == "TUTOR":
            return obj.pet.tutor == user

        if user.tipo == "VETERINARIO":
            return obj.veterinario == user

        return False


class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = (
        Agendamento.objects
        .select_related("pet__tutor", "pet", "veterinario", "servico")
        .all()
    )
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAdminOrTutor]
    pagination_class = None  

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        if user.is_staff:
            return qs.order_by("data_hora")

        if user.tipo == "TUTOR":
            return qs.filter(pet__tutor=user).order_by("data_hora")

        if user.tipo == "VETERINARIO":
            return qs.filter(veterinario=user).order_by("data_hora")

        return qs.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.tipo == "TUTOR":
            pet = serializer.validated_data.get("pet")

            if not pet:
                raise permissions.PermissionDenied("É necessário informar o pet.")

            if pet.tutor != user:
                raise permissions.PermissionDenied(
                    "Você só pode agendar consultas para seus próprios pets."
                )

            serializer.save(criado_por=user)

        else:
            serializer.save()

    def perform_update(self, serializer):
        user = self.request.user

        if user.tipo == "TUTOR":

            serializer.save()
        else:
            serializer.save()

    @action(detail=True, methods=["post"])
    def confirmar(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {"detail": "Apenas admin pode alterar status."},
                status=status.HTTP_403_FORBIDDEN
            )

        ag = self.get_object()
        ag.status = "confirmado"
        ag.save()
        return Response(self.get_serializer(ag).data)

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {"detail": "Apenas admin pode alterar status."},
                status=status.HTTP_403_FORBIDDEN
            )

        ag = self.get_object()
        ag.status = "cancelado"
        ag.save()
        return Response(self.get_serializer(ag).data)

    @action(detail=False, methods=["get"])
    def proximos(self, request):
        agora = timezone.now()

        qs = (
            self.get_queryset()
            .filter(
                data_hora__gte=agora,
                status__in=["pendente", "confirmado"]
            )
            .order_by("data_hora")[:10]
        )

        return Response(self.get_serializer(qs, many=True).data)
