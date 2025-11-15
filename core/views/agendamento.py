from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Count
from core.models import Agendamento, Veterinario
from core.serializers.agendamento import AgendamentoSerializer


class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        queryset = Agendamento.objects.select_related(
            'pet__tutor',
            'pet',
            'veterinario',
            'servico'
        )

        tutor_id = self.request.query_params.get('tutor_id')
        veterinario_id = self.request.query_params.get('veterinario_id')
        status_filter = self.request.query_params.get('status')
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')

        if tutor_id:
            queryset = queryset.filter(pet__tutor_id=tutor_id)

        if veterinario_id:
            queryset = queryset.filter(veterinario_id=veterinario_id)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if data_inicio:
            queryset = queryset.filter(data_hora__gte=data_inicio)

        if data_fim:
            queryset = queryset.filter(data_hora__lte=data_fim)

        return queryset.order_by('data_hora')

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        agendamento = self.get_object()
        agendamento.status = 'confirmado'
        agendamento.save()
        serializer = self.get_serializer(agendamento)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        agendamento = self.get_object()
        agendamento.status = 'cancelado'
        agendamento.save()
        serializer = self.get_serializer(agendamento)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def proximos(self, request):
        agora = timezone.now()
        agendamentos = (
            self.get_queryset()
            .filter(data_hora__gte=agora, status__in=['pendente', 'confirmado'])
            .order_by('data_hora')[:10]
        )
        serializer = self.get_serializer(agendamentos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_veterinario(self, request):
        veterinarios = Veterinario.objects.annotate(
            total_agendamentos=Count('agendamentos'),
            agendamentos_confirmados=Count(
                'agendamentos', filter=Q(agendamentos__status='confirmado')
            ),
            agendamentos_pendentes=Count(
                'agendamentos', filter=Q(agendamentos__status='pendente')
            ),
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
        response = super().list(request, *args, **kwargs)

        if isinstance(response.data, list):
            data = {
                'results': response.data,
                'metadata': {
                    'total': self.get_queryset().count(),
                    'filtros_aplicados': dict(request.query_params),
                    'timestamp': timezone.now().isoformat(),
                },
            }
            response.data = data
        else:
            response.data['metadata'] = {
                'total': self.get_queryset().count(),
                'filtros_aplicados': dict(request.query_params),
                'timestamp': timezone.now().isoformat(),
            }

        return response
