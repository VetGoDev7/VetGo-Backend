from rest_framework.viewsets import ModelViewSet
from core.models import Tutor
from core.serializers import TutorSerializer

class TutorViewSet(ModelViewSet):
    """
    ViewSet para gerenciar os tutores.
    Permite operações CRUD (Create, Read, Update, Delete) para o modelo Tutor.
    """
    queryset = Tutor.objects.all()  # Define a queryset que será usada para as operações
    serializer_class = TutorSerializer  # Define o serializer que será usado para validar e serializar os dados

    def perform_create(self, serializer):
        """
        Sobrescreve o método perform_create para adicionar lógica adicional ao criar um tutor.
        """
        serializer.save()  # Salva o novo tutor no banco de dados

    def perform_update(self, serializer):
        """
        Sobrescreve o método perform_update para adicionar lógica adicional ao atualizar um tutor.
        """
        serializer.save()  # Salva as alterações no tutor

    def perform_destroy(self, instance):
        """
        Sobrescreve o método perform_destroy para adicionar lógica adicional ao excluir um tutor.
        """
        instance.delete()  # Exclui o tutor do banco de dados
