from django.shortcuts import render, redirect
from apps.cart.cart import Cart
from .models import Order, OrderItem
from django.contrib import messages

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('catalog:home')

    if request.method == 'POST':
        name = request.POST.get('customer_name')
        email = request.POST.get('customer_email')
        phone = request.POST.get('customer_phone')
        
        # Cria o Pedido principal
        order = Order.objects.create(
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            subtotal=cart.get_total_price(),
            total=cart.get_total_price()  # Por enquanto, sem calculo de frete ou desconto
        )
        
        # Transfere itens do carrinho para o pedido
        for item in cart:
            OrderItem.objects.create(
                order=order,
                variant=item['variant'],
                price=item['price'],
                quantity=item['quantity']
            )
            
        # Limpa o carrinho
        cart.clear()
        
        # Em fase real, redirecionaria para gateway de pagamentos ou página de sucesso.
        messages.success(request, f"Pedido #{order.id} realizado com sucesso! Em breve um consultor entrará em contato.")
        return redirect('orders:checkout_success', order_id=order.id)
        
    return render(request, 'orders/checkout.html', {'cart': cart})

def checkout_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/success.html', {'order': order})
