from rest_framework.viewsets import ModelViewSet
from core.models import Veterinario
from core.serializers import VeterinarioSerializer


class VeterinarioViewSet(ModelViewSet):
    """
    ViewSet para gerenciar os veterinários.
    Permite operações CRUD (Create, Read, Update, Delete) para o modelo Veterinario.
    """

    queryset = Veterinario.objects.all()  # Define a queryset que será usada para as operações
    serializer_class = VeterinarioSerializer  # Define o serializer que será usado para validar e serializar os dados

    def perform_create(self, serializer):
        """
        Sobrescreve o método perform_create para adicionar lógica adicional ao criar um veterinário.
        """
        serializer.save()  # Salva o novo veterinário no banco de dados

    def perform_update(self, serializer):
        """
        Sobrescreve o método perform_update para adicionar lógica adicional ao atualizar um veterinário.
        """
        serializer.save()  # Salva as alterações no veterinário

    def perform_destroy(self, instance):
        """
        Sobrescreve o método perform_destroy para adicionar lógica adicional ao excluir um veterinário.
        """
        instance.delete()  # Exclui o veterinário do banco de dados
