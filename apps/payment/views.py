import mercadopago
import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from apps.orders.models import Order

logger = logging.getLogger(__name__)


def pay(request, order_id):
    """Página de pagamento: exibe opções Pix e Cartão via Checkout Pro do MP."""
    order = get_object_or_404(Order, id=order_id)

    # Gera a preferência no Mercado Pago se ainda não existir
    if not order.mp_preference_id:
        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

        items = []
        for item in order.items.select_related('variant__product'):
            items.append({
                "title": f"{item.variant.product.name} - {item.variant.size_label}",
                "quantity": item.quantity,
                "unit_price": float(item.price),
                "currency_id": "BRL",
            })

        # Adiciona frete como item separado se houver custo
        if order.shipping_cost > 0:
            items.append({
                "title": "Frete",
                "quantity": 1,
                "unit_price": float(order.shipping_cost),
                "currency_id": "BRL",
            })

        base_url = settings.SITE_URL  # ex: https://xxxxxx.ngrok-free.app
        preference_data = {
            "items": items,
            "payer": {
                "name": order.customer_name,
                "email": order.customer_email,
                "phone": {"area_code": "", "number": order.customer_phone},
            },
            "payment_methods": {
                "excluded_payment_types": [],
                "installments": 12,
            },
            "back_urls": {
                "success": f"{base_url}/pedidos/sucesso/{order.id}/",
                "failure": f"{base_url}/pagamento/{order.id}/",
                "pending": f"{base_url}/pedidos/sucesso/{order.id}/",
            },
            # "auto_return": "approved",
            # "notification_url": f"{base_url}/pagamento/webhook/",
            "external_reference": str(order.id),
            "statement_descriptor": "NGD Grafica",
        }

        result = sdk.preference().create(preference_data)
        preference = result.get("response", {})

        if result.get("status") == 201:
            order.mp_preference_id = preference["id"]
            order.save(update_fields=["mp_preference_id"])
        else:
            logger.error(f"Erro ao criar preferência MP: {result}")

    # Determina o link de checkout (sandbox vs produção)
    is_sandbox = getattr(settings, 'MP_SANDBOX', True)
    if is_sandbox:
        checkout_url = f"https://sandbox.mercadopago.com.br/checkout/v1/redirect?pref_id={order.mp_preference_id}"
    else:
        checkout_url = f"https://www.mercadopago.com.br/checkout/v1/redirect?pref_id={order.mp_preference_id}"

    context = {
        'order': order,
        'mp_public_key': settings.MP_PUBLIC_KEY,
        'preference_id': order.mp_preference_id,
        'checkout_url': checkout_url,
        'is_sandbox': is_sandbox,
    }
    return render(request, 'payment/payment.html', context)


@csrf_exempt
@require_POST
def webhook(request):
    """Recebe notificações IPN do Mercado Pago e atualiza o status do pedido."""
    try:
        # O MP envia JSON ou form-encoded dependendo do tipo de notificação
        topic = request.GET.get('topic') or request.POST.get('topic')
        resource_id = request.GET.get('id') or request.POST.get('data.id')

        # Notificação nova API (Webhooks v2)
        if not topic and request.content_type == 'application/json':
            body = json.loads(request.body)
            topic = body.get('type')
            resource_id = body.get('data', {}).get('id')

        if topic == 'payment' and resource_id:
            sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
            payment_info = sdk.payment().get(resource_id)
            payment = payment_info.get("response", {})

            if payment.get("status") == "approved":
                order_id = payment.get("external_reference")
                if order_id:
                    order = Order.objects.get(id=int(order_id))
                    order.status = 'pago'
                    order.mp_payment_id = str(resource_id)
                    order.save(update_fields=["status", "mp_payment_id"])
                    logger.info(f"Pedido #{order_id} marcado como PAGO via webhook MP.")

    except Exception as e:
        logger.error(f"Erro no webhook MP: {e}")

    return HttpResponse(status=200)
