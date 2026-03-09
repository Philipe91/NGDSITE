import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Category, Product, ProductVariant
from django.utils.text import slugify

cat, _ = Category.objects.get_or_create(name='Totens PDV', defaults={'slug': 'totens-pdv'})

totems = ['Totem Triangular', 'Totem Cubo', 'Totem Triedro', 'Totem Eleptico Lama', 'Totem Banana', 'Totem Replica']

for i, name in enumerate(totems):
    slug = slugify(name)
    prod, created = Product.objects.update_or_create(
        slug=slug,
        defaults={
            'name': name,
            'category': cat,
            'short_description': f'Expositor tipo {name} para pontos de venda com alta visibilidade.',
            'description': f'O {name} e ideal para campanhas promocionais. Facil de montar e com excelente acabamento.',
            'is_active': True,
        }
    )
    # Using get_or_create to avoid IntegrityError on sku, allowing updates on everything else if needed
    variant, var_created = ProductVariant.objects.get_or_create(
        sku=f'TM-PDV-{i+1:03d}',
        defaults={
            'product': prod,
            'size_label': 'Padrao',
            'width_cm': 60.00,
            'height_cm': 160.00,
            'price': 89.90
        }
    )
    # If variant exists but belongs to a different product, or we just want to ensure it belongs to this product:
    if not var_created and variant.product != prod:
        variant.product = prod
        variant.save()
        
    print(f'Ready: {name}')

print('DONE SEEDING')
