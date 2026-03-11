import os, sys, django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

image_mappings = {
    'totem_branded': r'c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\totem_branded_mockup.png',
    'cubo_branded':  r'c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\cubo_branded_mockup.png',
    'wobbler_branded': r'c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\wobbler_branded_mockup.png',
    'faixa_branded': r'c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\faixa_branded_mockup.png',
}

assignments = {
    'totem_branded': [1, 4, 5, 6, 7, 8, 9, 10], # Totens
    'cubo_branded': [2, 11], # Cubos
    'wobbler_branded': [3, 12], # Wobblers
    'faixa_branded': [13, 14], # Faixa/Stopper
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

print("Done updating realistic branded images.")
