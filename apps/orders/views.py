from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from apps.cart.cart import Cart
from .models import Order, OrderItem
from .shipping import get_shipping_options
from decimal import Decimal

CUSTOMER_SESSION_KEY = 'customer_email'
ALLOWED_ART_EXTENSIONS = {'.pdf', '.cdr', '.ai', '.jpg', '.jpeg', '.png'}


def _can_manage_order_art(request, order):
    if request.user.is_staff:
        return True

    customer_email = request.session.get(CUSTOMER_SESSION_KEY, '').strip().lower()
    if customer_email and customer_email == order.customer_email.strip().lower():
        return True

    if request.user.is_authenticated and request.user.email:
        return request.user.email.strip().lower() == order.customer_email.strip().lower()

    return False


def calcular_frete(request):
    """Endpoint AJAX — retorna opções de frete para o CEP informado."""
    cep = request.GET.get('cep', '').replace('-', '').strip()
    if len(cep) != 8 or not cep.isdigit():
        return JsonResponse({'error': 'CEP inválido. Informe 8 dígitos.'}, status=400)

    cart = Cart(request)
    options = get_shipping_options(cep, cart)
    return JsonResponse({
        'options': [
            {
                'id': o['id'],
                'label': o['label'],
                'description': o['description'],
                'cost': float(o['cost']),
                'days': o['days'],
            }
            for o in options
        ]
    })


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('catalog:home')

    if request.method == 'POST':
        name = request.POST.get('customer_name', '').strip()
        email = request.POST.get('customer_email', '').strip()
        phone = request.POST.get('customer_phone', '').strip()
        shipping_method = request.POST.get('shipping_method', 'retirada')
        shipping_cep = request.POST.get('shipping_cep', '').strip()
        shipping_address = request.POST.get('shipping_address', '').strip()
        shipping_cost = Decimal(request.POST.get('shipping_cost', '0.00'))

        subtotal = cart.get_total_price()
        total = subtotal + shipping_cost

        order = Order.objects.create(
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            shipping_method=shipping_method,
            shipping_cost=shipping_cost,
            shipping_cep=shipping_cep,
            shipping_address=shipping_address,
            subtotal=subtotal,
            total=total,
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                variant=item['variant'],
                price=item['price'],
                quantity=item['quantity'],
            )

        cart.clear()

        # Redireciona para pagamento (Fase 11)
        return redirect('payment:pay', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


def checkout_success(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__variant__product'), id=order_id)
    return render(request, 'orders/success.html', {'order': order})


def upload_art(request, order_id, item_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    order = get_object_or_404(Order.objects.prefetch_related('items'), id=order_id)
    item = get_object_or_404(OrderItem, id=item_id, order=order)

    if not _can_manage_order_art(request, order):
        return JsonResponse({'error': 'Você não tem permissão para enviar arte para este pedido.'}, status=403)

    uploaded_file = request.FILES.get('art_file')
    if not uploaded_file:
        return JsonResponse({'error': 'Selecione um arquivo para enviar.'}, status=400)

    file_name = uploaded_file.name.lower()
    extension = f".{file_name.rsplit('.', 1)[-1]}" if '.' in file_name else ''
    if extension not in ALLOWED_ART_EXTENSIONS:
        return JsonResponse({
            'error': 'Formato inválido. Envie PDF, CDR, AI, JPG ou PNG.'
        }, status=400)

    item.art_file = uploaded_file
    item.art_status = 'em_analise'
    item.save(update_fields=['art_file', 'art_status'])

    if order.status in {'aguardando_pagamento', 'pago', 'aguardando_arte'}:
        order.status = 'arte_recebida'
        order.save(update_fields=['status'])

    return JsonResponse({
        'success': True,
        'message': 'Arte enviada com sucesso. Nosso time já está analisando.',
        'file_name': item.art_file.name.split('/')[-1],
        'file_url': item.art_file.url,
        'art_status': item.get_art_status_display(),
    })
