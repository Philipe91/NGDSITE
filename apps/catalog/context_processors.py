from apps.catalog.models import Product, Category

def totens_processor(request):
    try:
        # Puxa os 6 primeiros totens para exibir no megamenu
        cat = Category.objects.get(slug='totens-pdv')
        totens = Product.objects.filter(category=cat, is_active=True).order_by('id')[:6]
    except Category.DoesNotExist:
        totens = []
    
    return {'mega_totens': totens}
