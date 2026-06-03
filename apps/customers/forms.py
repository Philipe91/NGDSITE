"""Form de cadastro customizado — adiciona campos profissionais (PF/PJ,
nome/razão, CPF/CNPJ, telefone) ao signup do allauth e cria o CustomerProfile."""
import re
from django import forms
from django.core.exceptions import ValidationError

from .models import CustomerProfile
from .validators import valida_documento


def _so_digitos(v: str) -> str:
    return re.sub(r'\D', '', v or '')


class CustomSignupForm(forms.Form):
    """Mixado pelo allauth no SignupForm (via ACCOUNT_SIGNUP_FORM_CLASS).
    Os campos abaixo aparecem JUNTO de email/senha. O método signup()
    é chamado pelo allauth após criar o User."""

    tipo_pessoa = forms.ChoiceField(
        choices=CustomerProfile.TIPO_CHOICES,
        initial=CustomerProfile.TIPO_PF,
        widget=forms.RadioSelect,
    )
    nome_razao = forms.CharField(
        max_length=180,
        label="Nome completo / Razão social",
        widget=forms.TextInput(attrs={'placeholder': 'Seu nome ou razão social'}),
    )
    cpf_cnpj = forms.CharField(
        max_length=18,
        label="CPF / CNPJ",
        widget=forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
    )
    telefone = forms.CharField(
        max_length=20,
        label="Telefone / WhatsApp",
        widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
    )

    field_order = ['tipo_pessoa', 'nome_razao', 'cpf_cnpj', 'telefone',
                   'email', 'password1', 'password2']

    def clean_nome_razao(self):
        nome = (self.cleaned_data.get('nome_razao') or '').strip()
        if len(nome) < 3:
            raise ValidationError("Informe o nome completo ou a razão social.")
        return nome

    def clean_telefone(self):
        tel = _so_digitos(self.cleaned_data.get('telefone'))
        if len(tel) < 10 or len(tel) > 11:
            raise ValidationError("Telefone inválido. Use DDD + número.")
        return self.cleaned_data.get('telefone').strip()

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo_pessoa')
        doc = cleaned.get('cpf_cnpj')
        if tipo and doc:
            try:
                valida_documento(tipo, doc)
            except ValidationError as e:
                self.add_error('cpf_cnpj', e)
        return cleaned

    def signup(self, request, user):
        """Chamado pelo allauth após criar o User. Cria o perfil + preenche
        o first_name do User (usado em saudações)."""
        nome = self.cleaned_data['nome_razao']
        user.first_name = nome.split(' ')[0][:30]
        user.save(update_fields=['first_name'])

        CustomerProfile.objects.update_or_create(
            user=user,
            defaults={
                'tipo_pessoa': self.cleaned_data['tipo_pessoa'],
                'nome_razao': nome,
                'cpf_cnpj': self.cleaned_data['cpf_cnpj'].strip(),
                'telefone': self.cleaned_data['telefone'].strip(),
            },
        )
        return user
