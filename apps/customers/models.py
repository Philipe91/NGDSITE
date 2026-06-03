from django.db import models
from django.contrib.auth.models import User


class CustomerProfile(models.Model):
    """Dados cadastrais do cliente para emissão de nota fiscal e contato.
    Vinculado 1:1 ao User do Django (login por e-mail/senha via allauth)."""

    TIPO_PF = 'PF'
    TIPO_PJ = 'PJ'
    TIPO_CHOICES = [
        (TIPO_PF, 'Pessoa Física'),
        (TIPO_PJ, 'Pessoa Jurídica'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile',
        verbose_name="Usuário",
    )
    tipo_pessoa = models.CharField(
        max_length=2, choices=TIPO_CHOICES, default=TIPO_PF,
        verbose_name="Tipo de pessoa",
    )
    nome_razao = models.CharField(
        max_length=180, blank=True,
        verbose_name="Nome completo / Razão social",
    )
    cpf_cnpj = models.CharField(
        max_length=18, blank=True, db_index=True,
        verbose_name="CPF / CNPJ",
        help_text="Usado para emissão de nota fiscal.",
    )
    telefone = models.CharField(
        max_length=20, blank=True,
        verbose_name="Telefone / WhatsApp",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil do Cliente"
        verbose_name_plural = "Perfis de Clientes"

    def __str__(self):
        return f"{self.nome_razao or self.user.email} ({self.get_tipo_pessoa_display()})"

    @property
    def documento_label(self):
        return "CNPJ" if self.tipo_pessoa == self.TIPO_PJ else "CPF"
