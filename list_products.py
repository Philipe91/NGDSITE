import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product
for p in Product.objects.all():
    img_name = p.featured_image.name if p.featured_image else "None"
    print(f"ID: {p.id} | Slug: {p.slug} | Name: {p.name} | Image: {img_name}")
