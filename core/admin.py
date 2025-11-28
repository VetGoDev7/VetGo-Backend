"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models
from core.models import Tutor, Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    fields = ['pet', 'veterinario', 'servico', 'data_hora', 'status']

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)

        pet_id = request.GET.get('pet')  

        if pet_id:
            initial['pet'] = pet_id

        return initial


# -------------------------------
#  ADMIN USER
# -------------------------------
def user_email(self, obj):
    return obj.user.email if obj.user else '-'


user_email.short_description = 'Email do Usuário'


class UserAdmin(BaseUserAdmin):
    """Define o admin do usuário."""

    ordering = ['id']
    list_display = ['email', 'name', 'is_staff']

    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'tipo')}),
        (_('Permissões'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Datas importantes'), {'fields': ('last_login',)}),
        (_('Grupos'), {'fields': ('groups',)}),
        (_('Permissões de usuário'), {'fields': ('user_permissions',)}),
    )

    readonly_fields = ['last_login']

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Pet)
admin.site.register(models.Veterinario)
admin.site.register(models.Servico)
