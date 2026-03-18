import requests
from django.conf import settings

def send_telegram_order_notification(order):
    """
    Envia notificação de venda aprovada para o grupo do Telegram.
    """
    bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
    
    if not bot_token or not chat_id:
        return False
        
    admin_url = f"{settings.SITE_URL}/admin/orders/order/{order.id}/change/"
        
    message = (
        f"🚀 <b>NOVA VENDA APROVADA!</b>\n\n"
        f"<b>Pedido:</b> #{order.id}\n"
        f"<b>Cliente:</b> {order.customer_name}\n"
        f"<b>Valor:</b> R$ {order.total}\n"
        f"<b>Entrega:</b> {order.shipping_method}\n\n"
        f"Ver no painel: <a href='{admin_url}'>Acessar Pedido</a>"
    )
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        requests.post(url, json=payload, timeout=5)
        return True
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")
        return False
