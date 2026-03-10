from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from apps.cart.cart import Cart
from .models import Order, OrderItem
from .shipping import get_shipping_options
from decimal import Decimal


def calcular_frete(request):
    """Endpoint AJAX — retorna opções de frete para o CEP informado."""
    cep = request.GET.get('cep', '').replace('-', '').strip()
    if len(cep) != 8 or not cep.isdigit():
        return JsonResponse({'error': 'CEP inválido. Informe 8 dígitos.'}, status=400)

    options = get_shipping_options(cep)
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
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/success.html', {'order': order})
