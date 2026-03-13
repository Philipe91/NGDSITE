from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from apps.orders.models import Order, OrderItem

CUSTOMER_SESSION_KEY = 'customer_email'


def _require_customer(request):
    """Retorna o email da sessão ou None se não logado."""
    return request.session.get(CUSTOMER_SESSION_KEY)


def login_view(request):
    """Login simples por e-mail (sem senha, baseado em pedidos existentes)."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if Order.objects.filter(customer_email__iexact=email).exists():
            request.session[CUSTOMER_SESSION_KEY] = email
            return redirect('customers:dashboard')
        else:
            messages.error(request, 'Nenhum pedido encontrado para este e-mail. Verifique o e-mail usado no checkout.')
    return render(request, 'customers/login.html')


def logout_view(request):
    """Limpa a sessão do cliente."""
    request.session.pop(CUSTOMER_SESSION_KEY, None)
    return redirect('catalog:home')


def my_account(request):
    """Painel do cliente — resumo dos pedidos."""
    email = _require_customer(request)
    if not email:
        return redirect('customers:login')

    orders = Order.objects.filter(customer_email__iexact=email).prefetch_related('items__variant__product').order_by('-created_at')
    active_count = orders.exclude(status__in=['entregue', 'cancelado']).count()
    total_count = orders.count()
    pending_art_count = OrderItem.objects.filter(
        order__customer_email__iexact=email,
        art_status='pendente'
    ).count()

    context = {
        'customer_email': email,
        'customer_name': orders.first().customer_name if orders.exists() else email,
        'orders': orders[:5],
        'active_count': active_count,
        'total_count': total_count,
        'pending_art_count': pending_art_count,
    }
    return render(request, 'customers/my_account.html', context)


def my_orders(request):
    """Lista completa de pedidos do cliente."""
    email = _require_customer(request)
    if not email:
        return redirect('customers:login')

    orders = Order.objects.filter(
        customer_email__iexact=email
    ).prefetch_related('items__variant__product').order_by('-created_at')

    context = {
        'customer_email': email,
        'customer_name': orders.first().customer_name if orders.exists() else email,
        'orders': orders,
    }
    return render(request, 'customers/my_orders.html', context)


def order_detail(request, order_id):
    """Detalhe de um pedido específico com rastreamento e upload de arte."""
    email = _require_customer(request)
    if not email:
        return redirect('customers:login')

    order = get_object_or_404(Order, id=order_id, customer_email__iexact=email)

    # Define os passos do rastreamento
    STEPS = [
        ('aguardando_pagamento', 'Aguardando Pagamento', 'Confirme o pagamento para iniciarmos.'),
        ('pago',                'Pagamento Confirmado', 'Pagamento recebido com sucesso!'),
        ('aguardando_arte',     'Aguardando Arte',      'Envie o arquivo de arte para produção.'),
        ('arte_recebida',       'Arte Recebida',        'Sua arte está sendo revisada pela nossa equipe.'),
        ('em_producao',         'Em Produção',          'Seu material está sendo fabricado!'),
        ('enviado',             'Enviado',              'Pacote enviado. Em breve chegará até você.'),
        ('entregue',            'Entregue',             'Pedido entregue com sucesso!'),
    ]

    status_order = [s[0] for s in STEPS]
    try:
        current_step = status_order.index(order.status)
    except ValueError:
        current_step = 0

    context = {
        'customer_email': email,
        'customer_name': order.customer_name,
        'order': order,
        'steps': STEPS,
        'status_order': status_order,
        'current_step': current_step,
    }
    return render(request, 'customers/order_detail.html', context)


def upload_art(request, item_id):
    """Re-upload de arte para um item de pedido pelo cliente."""
    email = _require_customer(request)
    if not email:
        return redirect('customers:login')

    item = get_object_or_404(OrderItem, id=item_id, order__customer_email__iexact=email)

    # Só permite reenvio se a arte foi rejeitada ou ainda está pendente
    if item.art_status not in ['pendente', 'rejeitado']:
        messages.error(request, 'Este item não permite novo envio de arte no momento.')
        return redirect('customers:order_detail', order_id=item.order.id)

    if request.method == 'POST' and request.FILES.get('art_file'):
        item.art_file = request.FILES['art_file']
        item.art_status = 'em_analise'
        item.save()
        messages.success(request, 'Arte enviada com sucesso! Nossa equipe irá analisar em breve.')

        # Notifica equipe interna por e-mail
        try:
            send_mail(
                subject=f'[NGD] Nova arte enviada — Pedido #{item.order.id}',
                message=(
                    f'Cliente: {item.order.customer_name}\n'
                    f'E-mail: {item.order.customer_email}\n'
                    f'Pedido: #{item.order.id}\n'
                    f'Item: {item.variant}\n\n'
                    f'Acesse o admin para revisar o arquivo.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        return redirect('customers:order_detail', order_id=item.order.id)

    messages.error(request, 'Nenhum arquivo selecionado.')
    return redirect('customers:order_detail', order_id=item.order.id)
