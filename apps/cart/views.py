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
    
    if not variant_id:
        messages.error(request, "Por favor, selecione um formato antes de adicionar ao carrinho.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
        
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart.add(variant=variant, quantity=quantity, update_quantity=True)
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
