from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from core.models import Agendamento
from core.serializers import AgendamentoSerializer


class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        """
        Personaliza o queryset baseado no usuário e parâmetros
        """
        queryset = Agendamento.objects.select_related('tutor', 'pet', 'veterinario', 'servico').prefetch_related(
            'tutor__user'
        )

        # Filtros por parâmetros de query
        tutor_id = self.request.query_params.get('tutor_id')
        veterinario_id = self.request.query_params.get('veterinario_id')
        status_filter = self.request.query_params.get('status')
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')

        if tutor_id:
            queryset = queryset.filter(tutor_id=tutor_id)

        if veterinario_id:
            queryset = queryset.filter(veterinario_id=veterinario_id)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if data_inicio:
            queryset = queryset.filter(data_hora__gte=data_inicio)

        if data_fim:
            queryset = queryset.filter(data_hora__lte=data_fim)

        # Ordenação padrão por data/hora
        queryset = queryset.order_by('data_hora')

        return queryset

    def perform_create(self, serializer):
        """
        Hook personalizado para criação de agendamentos
        """
        # Pode adicionar lógica adicional aqui
        serializer.save()

    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        """
        Ação customizada para confirmar um agendamento
        """
        agendamento = self.get_object()
        agendamento.status = 'confirmado'
        agendamento.save()

        serializer = self.get_serializer(agendamento)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """
        Ação customizada para cancelar um agendamento
        """
        agendamento = self.get_object()
        agendamento.status = 'cancelado'
        agendamento.save()

        serializer = self.get_serializer(agendamento)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def proximos(self, request):
        """
        Retorna os agendamentos futuros
        """
        agora = timezone.now()
        agendamentos = (
            self.get_queryset()
            .filter(data_hora__gte=agora, status__in=['pendente', 'confirmado'])
            .order_by('data_hora')[:10]
        )  # Limita a 10 resultados

        serializer = self.get_serializer(agendamentos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_veterinario(self, request):
        """
        Retorna estatísticas de agendamentos por veterinário
        """
        from django.db.models import Count
        from core.models import Veterinario

        veterinarios = Veterinario.objects.annotate(
            total_agendamentos=Count('agendamentos'),
            agendamentos_confirmados=Count('agendamentos', filter=Q(agendamentos__status='confirmado')),
            agendamentos_pendentes=Count('agendamentos', filter=Q(agendamentos__status='pendente')),
        )

        data = []
        for vet in veterinarios:
            data.append({
                'veterinario': vet.user.nome_completo if hasattr(vet, 'user') else 'N/A',
                'especialidade': vet.especialidade,
                'total_agendamentos': vet.total_agendamentos,
                'confirmados': vet.agendamentos_confirmados,
                'pendentes': vet.agendamentos_pendentes,
            })

        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        Personaliza a listagem de agendamentos
        """
        response = super().list(request, *args, **kwargs)

        # Adiciona metadados à resposta
        response.data['metadata'] = {
            'total': self.get_queryset().count(),
            'filtros_aplicados': dict(request.query_params),
            'timestamp': timezone.now().isoformat(),
        }

        return response
