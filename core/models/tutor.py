from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import make_password
from django import forms


class Tutor(models.Model):
    nome_completo = models.CharField(max_length=45, verbose_name='Nome Completo')
    email = models.EmailField(max_length=45, unique=True, validators=[EmailValidator()], verbose_name='E-mail')
    senha = models.CharField(max_length=128, verbose_name='Senha', null=True, blank=True)

    def __str__(self):
        return self.nome_completo

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)


class TutorForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Senha', required=False)


confirmar_senha = forms.CharField(widget=forms.PasswordInput, label='Confirmar Senha')


class Meta:
    model = Tutor
    fields = ['nome_completo', 'email', 'senha']


def clean(self):
    cleaned_data = super().clean()
    senha = cleaned_data.get('senha')
    confirmar_senha = cleaned_data.get('confirmar_senha')

    if senha and confirmar_senha and senha != confirmar_senha:
        raise forms.ValidationError('As senhas não coincidem.')

    return cleaned_data


def save(self, commit=True):
    tutor = super().save(commit=False)
    tutor.set_password(self.cleaned_data['senha'])
    if commit:
        tutor.save()
    return tutor
