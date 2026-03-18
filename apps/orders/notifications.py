import requests
from django.conf import settings

def send_telegram_message(text):
    """Envia mensagem de texto simples para o Telegram."""
    bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    chat_id   = getattr(settings, 'TELEGRAM_CHAT_ID', None)
    if not bot_token or not chat_id:
        return False
    try:
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=5,
        )
        return True
    except Exception as e:
        print(f"Erro Telegram: {e}")
        return False

def send_telegram_order_notification(order):
    """Envia notificação de venda aprovada para o grupo do Telegram."""
    admin_url = f"{settings.SITE_URL}/admin/orders/order/{order.id}/change/"
    message = (
        f"<b>NOVA VENDA APROVADA!</b>\n\n"
        f"<b>Pedido:</b> #{order.id}\n"
        f"<b>Cliente:</b> {order.customer_name}\n"
        f"<b>Valor:</b> R$ {order.total}\n"
        f"<b>Entrega:</b> {order.shipping_method}\n\n"
        f"Ver no painel: <a href='{admin_url}'>Acessar Pedido</a>"
    )
    return send_telegram_message(message)
