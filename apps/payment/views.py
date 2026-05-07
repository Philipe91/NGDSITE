import mercadopago
import json
import hmac
import hashlib
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from apps.orders.models import Order
from apps.orders.emails import send_payment_approved_email

logger = logging.getLogger(__name__)


def _validate_mp_signature(request, resource_id):
    """Valida a assinatura HMAC-SHA256 enviada pelo Mercado Pago no header x-signature.

    Formato esperado do header: "ts=<timestamp>,v1=<hash>"
    Manifest assinado: "id:<data.id>;request-id:<x-request-id>;ts:<ts>;"

    Em DEBUG ou quando MP_WEBHOOK_SECRET não está configurado, apenas registra um aviso e
    permite o webhook (modo de desenvolvimento). Em produção com secret definido, é obrigatório.
    """
    secret = getattr(settings, "MP_WEBHOOK_SECRET", "")

    if not secret:
        if settings.DEBUG:
            logger.warning("MP_WEBHOOK_SECRET ausente — aceitando webhook em modo dev. Configure antes de produção.")
            return True
        logger.error("MP_WEBHOOK_SECRET não configurado em produção. Webhook rejeitado.")
        return False

    x_signature = request.headers.get("x-signature", "")
    x_request_id = request.headers.get("x-request-id", "")

    if not x_signature or not resource_id:
        logger.warning("Webhook MP sem x-signature ou resource_id.")
        return False

    parts = {}
    for piece in x_signature.split(","):
        if "=" in piece:
            k, v = piece.split("=", 1)
            parts[k.strip()] = v.strip()

    ts = parts.get("ts", "")
    received_hash = parts.get("v1", "")
    if not ts or not received_hash:
        logger.warning("Webhook MP com x-signature malformado.")
        return False

    manifest = f"id:{resource_id};request-id:{x_request_id};ts:{ts};"
    expected_hash = hmac.new(
        secret.encode("utf-8"),
        manifest.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_hash, received_hash):
        logger.warning("Assinatura HMAC do webhook MP inválida.")
        return False

    return True


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
@ratelimit(key='ip', rate='120/m', block=True)
def webhook(request):
    """Recebe notificações IPN do Mercado Pago e atualiza o status do pedido.

    Validação em camadas:
      1) HMAC-SHA256 do x-signature contra MP_WEBHOOK_SECRET (única fonte de confiança).
      2) Re-consulta da payment via SDK (não confia no payload do request).
      3) Conferência do valor pago contra Order.total (anti-fraude / anti-replay).
    """
    try:
        topic = request.GET.get('topic') or request.POST.get('topic')
        resource_id = request.GET.get('id') or request.POST.get('data.id')

        # Notificação nova API (Webhooks v2) — payload em JSON
        if not topic and request.content_type == 'application/json':
            try:
                body = json.loads(request.body or b"{}")
            except json.JSONDecodeError:
                return HttpResponse(status=400)
            topic = body.get('type')
            resource_id = body.get('data', {}).get('id')

        # Valida assinatura ANTES de tocar no banco / SDK
        if not _validate_mp_signature(request, resource_id):
            return HttpResponse(status=401)

        if topic == 'payment' and resource_id:
            sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
            payment_info = sdk.payment().get(resource_id)
            payment = payment_info.get("response", {})

            if payment.get("status") == "approved":
                order_id = payment.get("external_reference")
                if not order_id:
                    return HttpResponse(status=200)

                try:
                    order = Order.objects.get(id=int(order_id))
                except (Order.DoesNotExist, ValueError, TypeError):
                    logger.warning(f"Webhook MP referenciou order inexistente: {order_id}")
                    return HttpResponse(status=200)

                # Anti-fraude: o valor aprovado precisa bater com o total do pedido
                paid_amount = payment.get("transaction_amount")
                try:
                    from decimal import Decimal
                    if paid_amount is not None and Decimal(str(paid_amount)) < order.total:
                        logger.error(
                            f"Pedido #{order.id}: valor pago ({paid_amount}) menor que total ({order.total}). Recusado."
                        )
                        return HttpResponse(status=200)
                except Exception:
                    pass

                # Idempotência: se já está pago com mesmo payment_id, ignora
                if order.status == 'pago' and order.mp_payment_id == str(resource_id):
                    return HttpResponse(status=200)

                order.status = 'pago'
                order.mp_payment_id = str(resource_id)
                order.save(update_fields=["status", "mp_payment_id"])
                logger.info(f"Pedido #{order_id} marcado como PAGO via webhook MP.")
                send_payment_approved_email(order)

                try:
                    from apps.orders.notifications import send_telegram_order_notification
                    send_telegram_order_notification(order)
                except Exception as t_err:
                    logger.error(f"Erro Telegram hook: {t_err}")

    except Exception as e:
        logger.exception(f"Erro no webhook MP: {e}")

    return HttpResponse(status=200)
