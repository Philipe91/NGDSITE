import os, sys, django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

image_mappings = {
    'totem_pol': r'c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\totem_colored_brand.png',
    'cubo_pol':  r'c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\cubo_colored_brand.png',
    'wobbler_pol': r'c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\wobbler_colored_brand.png',
    'faixa_pol': r'c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\faixa_colored_brand.png',
}

assignments = {
    'totem_pol': [1, 4, 5, 6, 7, 8, 9, 10], # Totens
    'cubo_pol': [2, 11], # Cubos
    'wobbler_pol': [3, 12], # Wobblers
    'faixa_pol': [13, 14], # Faixa/Stopper
}

for img_key, product_ids in assignments.items():
    img_path = image_mappings[img_key]
    if os.path.exists(img_path):
        for pid in product_ids:
            try:
                p = Product.objects.get(id=pid)
                with open(img_path, 'rb') as f:
                    # Save under a new path
                    p.featured_image.save(os.path.basename(img_path), File(f), save=True)
                print(f"Updated product {p.name} with {img_key}")
            except Product.DoesNotExist:
                print(f"Product ID {pid} not found")
    else:
        print(f"Image not found: {img_path}")

print("Done updating colored images.")
