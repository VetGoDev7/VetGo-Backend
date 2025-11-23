from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Tutor
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        senha = request.data.get('senha')

        try:
            tutor = Tutor.objects.get(email=email)
        except Tutor.DoesNotExist:
            return Response({'erro': 'Email ou senha incorretos.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(senha, tutor.senha):
            return Response({'erro': 'Email ou senha incorretos.'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(tutor)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'tutor': {'id': tutor.id, 'nome_completo': tutor.nome_completo, 'email': tutor.email},
        })
