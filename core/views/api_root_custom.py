from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root_custom(request, format=None):
    return Response({
        'usuarios': reverse('usuarios-list', request=request, format=format),
        'tutores': reverse('tutor-list', request=request, format=format),
        'pets': reverse('pet-list', request=request, format=format),
        'veterinarios': reverse('veterinario-list', request=request, format=format),
        'servicos': reverse('servico-list', request=request, format=format),
        'agendamentos': reverse('agendamento-list', request=request, format=format),
    })
