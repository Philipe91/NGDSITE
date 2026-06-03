from django.contrib import admin
from .models import CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('nome_razao', 'tipo_pessoa', 'cpf_cnpj', 'telefone', 'user_email', 'created_at')
    list_filter = ('tipo_pessoa', 'created_at')
    search_fields = ('nome_razao', 'cpf_cnpj', 'telefone', 'user__email')
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "E-mail (login)"
