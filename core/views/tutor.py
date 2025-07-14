from rest_framework.viewsets import ModelViewSet

from core.models import Tutor
from core.serializers import TutorSerializer


class TutorViewSet(ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
