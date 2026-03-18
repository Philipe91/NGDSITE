"""
Portal de Aprovação de Arte — Fase 15
O cliente recebe um link com token único e pode aprovar ou rejeitar a arte
sem precisar de login.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from .models import OrderItem, Order
from .notifications import send_telegram_message


def art_approval_view(request, token):
    """Página pública onde o cliente visualiza e aprova/rejeita a arte."""
    item = get_object_or_404(OrderItem, art_approval_token=token)
    order = item.order
    return render(request, 'orders/art_approval.html', {
        'item': item,
        'order': order,
    })


def art_approve(request, token):
    """Cliente clica em Aprovar Arte."""
    item = get_object_or_404(OrderItem, art_approval_token=token)
    order = item.order

    item.art_status = 'aprovado'
    item.art_rejection_reason = ''
    item.save(update_fields=['art_status', 'art_rejection_reason'])

    # Atualiza status do pedido para em_producao se todos os itens aprovados
    all_items = order.items.all()
    if all(i.art_status == 'aprovado' for i in all_items):
        order.status = 'em_producao'
        order.save(update_fields=['status'])

    # Notifica via Telegram
    try:
        msg = (
            f"Arte APROVADA pelo cliente!\n"
            f"OS #{order.id} – {order.customer_name}\n"
            f"Item: {item.variant.product.name if item.variant else 'Produto'}"
        )
        send_telegram_message(msg)
    except Exception:
        pass

    return render(request, 'orders/art_approval_done.html', {
        'action': 'approved',
        'order': order,
    })


def art_reject(request, token):
    """Cliente clica em Solicitar Alteração."""
    item = get_object_or_404(OrderItem, art_approval_token=token)
    order = item.order
    reason = request.POST.get('reason', '').strip()

    item.art_status = 'rejeitado'
    item.art_rejection_reason = reason
    item.save(update_fields=['art_status', 'art_rejection_reason'])

    # Reverte status do pedido para arte_recebida
    if order.status == 'em_producao':
        order.status = 'arte_recebida'
        order.save(update_fields=['status'])

    # Notifica via Telegram
    try:
        msg = (
            f"Arte REJEITADA pelo cliente!\n"
            f"OS #{order.id} – {order.customer_name}\n"
            f"Motivo: {reason or 'Não informado'}"
        )
        send_telegram_message(msg)
    except Exception:
        pass

    return render(request, 'orders/art_approval_done.html', {
        'action': 'rejected',
        'order': order,
        'reason': reason,
    })


@staff_member_required
def send_art_approval_email_view(request, item_id):
    """Ação chamada pelo admin para enviar o link de aprovação por e-mail."""
    item  = get_object_or_404(OrderItem, id=item_id)
    order = item.order

    token_url = request.build_absolute_uri(
        reverse('orders:art_approval', kwargs={'token': item.art_approval_token})
    )

    subject = f"NGD – Aprovação de Arte: Pedido #{order.id}"
    html_content = render_to_string('emails/art_approval_email.html', {
        'order': order,
        'item': item,
        'approval_url': token_url,
        'site_url': settings.SITE_URL,
    })

    msg = EmailMultiAlternatives(
        subject,
        f"Acesse o link para aprovar sua arte: {token_url}",
        settings.DEFAULT_FROM_EMAIL,
        [order.customer_email],
    )
    msg.attach_alternative(html_content, 'text/html')
    try:
        msg.send(fail_silently=False)
        messages.success(request, f"E-mail de aprovação enviado para {order.customer_email}!")
    except Exception as e:
        messages.error(request, f"Erro ao enviar e-mail: {e}")

    # Redireciona de volta para a O.S.
    return redirect(f"/admin/orders/order/{order.id}/change/")
