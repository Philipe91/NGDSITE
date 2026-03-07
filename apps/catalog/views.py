from django.shortcuts import get_object_or_404, render
from .models import Product, Category

def home(request):
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    if not featured_products:
        # Fallback se não tiver destaques ainda
        featured_products = Product.objects.filter(is_active=True)[:8]
        
    context = {
        'categories': categories,
        'featured_products': featured_products
    }
    return render(request, 'catalog/home.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    variants = product.variants.filter(is_active=True).order_by('price')
    images = product.images.all()
    
    context = {
        'product': product,
        'variants': variants,
        'images': images,
    }
    return render(request, 'catalog/product_detail.html', context)
