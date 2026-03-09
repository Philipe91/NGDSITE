from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from apps.catalog.models import ProductVariant
from .cart import Cart
from django.contrib import messages

@require_POST
def cart_add(request):
    cart = Cart(request)
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))
    
    # Process production time fee
    try:
        prazo_str = request.POST.get('prazo', 'normal')
        if prazo_str.isdigit():
            prazo = int(prazo_str)
        else:
            prazo = 0 # Default/normal
    except ValueError:
        prazo = 0

    if not variant_id:
        messages.error(request, "Por favor, selecione um formato antes de adicionar ao carrinho.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
        
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart.add(variant=variant, quantity=quantity, update_quantity=True)
    
    # Base price calculation
    base_price = float(variant.price)
    discount_multiplier = 1.0
    
    # Apply quantity discounts
    if quantity >= 10:
        discount_multiplier = 0.85
    elif quantity >= 5:
        discount_multiplier = 0.90
    elif quantity >= 2:
        discount_multiplier = 0.95
        
    # Apply express delivery fees based on 'prazo'
    express_fee = 0
    if variant.product.slug == 'banner-rollup':
        if prazo == 6: express_fee = 20
        elif prazo == 5: express_fee = 40
        elif prazo == 4: express_fee = 60
        elif prazo == 3: express_fee = 80
        elif prazo == 2: express_fee = 100
        
    final_unit_price = (base_price * discount_multiplier) + express_fee
    
    # Ensure final unit price is updated in cart
    cart.update_price(variant, final_unit_price)

    messages.success(request, f"{quantity}x {variant.product.name} ({variant.size_label}) adicionado ao carrinho.")
    return redirect('cart:cart_detail')

def cart_remove(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart.remove(variant)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
