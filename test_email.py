import os
import django
from django.core.mail import send_mail
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

try:
    print(f"Tentando conectar ao SMTP: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
    print(f"Usando o usuario: {settings.EMAIL_HOST_USER}")
    send_mail(
        subject='NGD - Teste de Sistema Finalizado (Fase 14) 🚀',
        message='Se você está lendo isso, a nossa integração SMTP de E-mails Transacionais do E-commerce NGD foi um sucesso absoluto!\n\nAgora seus clientes receberão automaticamente:\n- Aviso de Pedido Recebido\n- Aviso de Pagamento Aprovado\n- Aviso de Envio para Transportadora / Liberação para Retirada',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['philipe.fernandes0101@gmail.com'],
        fail_silently=False,
    )
    print("E-mail enviado com sucesso! Verifique a caixa de entrada.")
except Exception as e:
    print(f"Erro ao enviar o e-mail: {e}")
