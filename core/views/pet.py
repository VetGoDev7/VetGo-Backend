from rest_framework.viewsets import ModelViewSet
from core.models import Pet
from core.serializers import PetSerializer

class PetViewSet(ModelViewSet):
    """
    ViewSet para gerenciar os pets.
    Permite operações CRUD (Create, Read, Update, Delete) para o modelo Pet.
    """
    queryset = Pet.objects.all()  # Define a queryset que será usada para as operações
    serializer_class = PetSerializer  # Define o serializer que será usado para validar e serializar os dados

    def perform_create(self, serializer):
        """
        Sobrescreve o método perform_create para adicionar lógica adicional ao criar um pet.
        """
        serializer.save()  # Salva o novo pet no banco de dados

    def perform_update(self, serializer):
        """
        Sobrescreve o método perform_update para adicionar lógica adicional ao atualizar um pet.
        """
        serializer.save()  # Salva as alterações no pet

    def perform_destroy(self, instance):
        """
        Sobrescreve o método perform_destroy para adicionar lógica adicional ao excluir um pet.
        """
        instance.delete()  # Exclui o pet do banco de dados
