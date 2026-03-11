import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.test import Client
from apps.catalog.models import ProductVariant

c = Client()
v = ProductVariant.objects.first()

response = c.post('/carrinho/adicionar/', {
    'variant_id': str(v.id),
    'quantity': '2',
    'prazo': 'normal'
})

print("Status code:", response.status_code)
if response.status_code == 200:
    print(response.content[:500])
elif response.status_code == 302:
    print("Redirect to:", response['Location'])
else:
    print(response.content.decode('utf-8'))
