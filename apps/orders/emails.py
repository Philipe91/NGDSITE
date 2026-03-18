from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order

def send_transactional_email(subject, template_name, context, to_email):
    html_content = render_to_string(template_name, context)
    text_content = f"Olá, saudações da NGD! Este é um email sobre seu pedido.\nRastreamento/Detalhes disponíveis em sua conta."
    from_email = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    
    try:
        msg.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

def send_order_created_email(order):
    subject = f"NGD - Pedido #{order.id} Recebido com Sucesso!"
    context = {
        'order': order,
        'site_url': settings.SITE_URL,
    }
    return send_transactional_email(subject, 'emails/order_created.html', context, order.customer_email)

def send_payment_approved_email(order):
    subject = f"NGD - Pagamento Aprovado! Pedido #{order.id}"
    context = {
        'order': order,
        'site_url': settings.SITE_URL,
    }
    return send_transactional_email(subject, 'emails/payment_approved.html', context, order.customer_email)

def send_order_shipped_email(order):
    subject = f"NGD - Seu Pedido #{order.id} foi Enviado/Liberado!"
    context = {
        'order': order,
        'site_url': settings.SITE_URL,
    }
    return send_transactional_email(subject, 'emails/order_shipped.html', context, order.customer_email)

def send_status_update_email(order, message):
    subject = f"NGD - Atualização: Pedido #{order.id}"
    context = {
        'order': order,
        'custom_message': message,
        'site_url': settings.SITE_URL,
    }
    return send_transactional_email(subject, 'emails/order_status_update.html', context, order.customer_email)
