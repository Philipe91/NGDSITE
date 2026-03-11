import os, sys, django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

image_mappings = {
    'totem_pol': r'C:\Users\Pc Fechamento\.gemini\antigravity\brain\3c3c17f7-70b3-42a3-ac4d-0994f66701fe\totem_poliondas_1773236276645.png',
    'cubo_pol': r'C:\Users\Pc Fechamento\.gemini\antigravity\brain\3c3c17f7-70b3-42a3-ac4d-0994f66701fe\cubo_poliondas_1773236314022.png',
    'wobbler_pol': r'C:\Users\Pc Fechamento\.gemini\antigravity\brain\3c3c17f7-70b3-42a3-ac4d-0994f66701fe\wobbler_poliondas_1773236338955.png',
    'faixa_pol': r'C:\Users\Pc Fechamento\.gemini\antigravity\brain\3c3c17f7-70b3-42a3-ac4d-0994f66701fe\faixa_poliondas_1773236359461.png',
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
                    p.featured_image.save(os.path.basename(img_path), File(f), save=True)
                print(f"Updated product {p.name} with {img_key}")
            except Product.DoesNotExist:
                print(f"Product ID {pid} not found")
    else:
        print(f"Image not found: {img_path}")

print("Done updating images.")
