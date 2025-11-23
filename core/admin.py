"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models
from core.models import Tutor


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'user_email']
    search_fields = ['nome_completo', 'user__email']

    def user_email(self, obj):
        return obj.user.email if obj.user else '-'
    user_email.short_description = 'Email do Usuário'


class UserAdmin(BaseUserAdmin):
    """Define o admin do usuário."""

    ordering = ['id']
    list_display = ['email', 'name', 'is_staff']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações pessoais'), {'fields': ('name', 'passage_id')}),
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
admin.site.register(models.Agendamento)
admin.site.register(models.Pet)
admin.site.register(models.Veterinario)
admin.site.register(models.Servico)
