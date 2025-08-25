from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter


from core.views import UserViewSet, TutorViewSet, PetViewSet, VeterinarioViewSet, ServicoViewSet, AgendamentoViewSet

router = DefaultRouter()

router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register(r'tutores', TutorViewSet, basename='tutor')
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'veterinarios', VeterinarioViewSet, basename='veterinario')
router.register(r'servicos', ServicoViewSet, basename='servico')
router.register(r'agendamentos', AgendamentoViewSet, basename='agendamento')

urlpatterns = [
    path('admin/', admin.site.urls),
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    # API
    path('api/', include(router.urls)),
]
