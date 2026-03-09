import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

products = Product.objects.filter(featured_image__exact='') | Product.objects.filter(featured_image__isnull=True)
print("Products without images:")
for p in products:
    print(f"ID: {p.id} | Slug: {p.slug} | Name: {p.name}")
