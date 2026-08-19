import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product, ProductVariant

p = Product.objects.get(slug='banner-rollup')

variants_data = [
    {
        "sku": "ROLL-80X200",
        "size_label": "80 x 200 cm ou 85 x 200 cm",
        "price": 329.90,
        "width_cm": 85.0,
        "height_cm": 200.0,
        "weight_kg": 3.0,
        "length_cm": 85.0
    },
    {
        "sku": "ROLL-100X200",
        "size_label": "100 x 200 cm",
        "price": 429.90,
        "width_cm": 100.0,
        "height_cm": 200.0,
        "weight_kg": 3.5,
        "length_cm": 100.0
    },
    {
        "sku": "ROLL-120X200",
        "size_label": "120 x 200 cm",
        "price": 549.90,
        "width_cm": 120.0,
        "height_cm": 200.0,
        "weight_kg": 4.0,
        "length_cm": 120.0
    },
    {
        "sku": "ROLL-150X200",
        "size_label": "150 x 200 cm",
        "price": 699.90,
        "width_cm": 150.0,
        "height_cm": 200.0,
        "weight_kg": 5.0,
        "length_cm": 150.0
    }
]

# Wipe old variants for this specific product to ensure a clean state
ProductVariant.objects.filter(product=p).delete()

for v in variants_data:
    ProductVariant.objects.create(
        product=p,
        sku=v["sku"],
        size_label=v["size_label"],
        price=v["price"],
        width_cm=v["width_cm"],
        height_cm=v["height_cm"],
        weight_kg=v["weight_kg"],
        length_cm=v["length_cm"]
    )

print("Rollup variants have been updated successfully.")
