"""Atualiza dados do produto Faixa de Gôndola (Régua) com variantes e descrições."""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from decimal import Decimal
from apps.catalog.models import Product, ProductVariant

SLUG = 'faixa-de-gondola-regua'

p = Product.objects.get(slug=SLUG)

p.short_description = (
    "Régua/Faixa de Gôndola em poliondas para sinalização de prateleira. "
    "Material resistente, leve e fácil de fixar. Personalização total nas "
    "duas faces — ideal para destacar ofertas, descontos e marcas."
)
p.description = (
    "Faixa de Gôndola (Régua) NGD em polipropileno corrugado (poliondas) "
    "de 3mm. Formato horizontal compacto, perfeita para encaixar em "
    "prateleiras de supermercados, lojas e PDV em geral.\n\n"
    "Impressão UV em alta resolução, cores vivas e acabamento fosco. "
    "Material leve, resistente à umidade e durável — substitui o papelão "
    "com sobra. Tamanhos disponíveis: 60×10, 90×10 e 120×10 cm."
)
p.meta_title = "Faixa de Gôndola (Régua) em Poliondas Personalizada | NGD"
p.meta_description = (
    "Régua de gôndola em poliondas 3mm para sinalização de prateleira. "
    "Tamanhos 60×10, 90×10 e 120×10 cm. Impressão UV. Envio para todo Brasil."
)
p.save()
print(f'OK Produto atualizado: {p.name}')

VARIANTS = [
    dict(sku='NGD-FAIXA-GONDOLA-60X10',  size_label='60x10 cm',
         width_cm=Decimal('60.00'),  height_cm=Decimal('10.00'),
         length_cm=Decimal('15.00'), weight_kg=Decimal('0.080'),
         price=Decimal('8.90')),
    dict(sku='NGD-FAIXA-GONDOLA-90X10',  size_label='90x10 cm',
         width_cm=Decimal('90.00'),  height_cm=Decimal('10.00'),
         length_cm=Decimal('15.00'), weight_kg=Decimal('0.120'),
         price=Decimal('11.90')),
    dict(sku='NGD-FAIXA-GONDOLA-120X10', size_label='120x10 cm',
         width_cm=Decimal('120.00'), height_cm=Decimal('10.00'),
         length_cm=Decimal('15.00'), weight_kg=Decimal('0.160'),
         price=Decimal('14.90')),
]

new_skus = {v['sku'] for v in VARIANTS}
old = p.variants.exclude(sku__in=new_skus)
for sku in old.values_list('sku', flat=True):
    print(f'  - removida variante antiga: {sku}')
old.delete()

for data in VARIANTS:
    v, created = ProductVariant.objects.update_or_create(
        product=p, sku=data['sku'],
        defaults={**data, 'is_active': True},
    )
    tag = 'CREATED' if created else 'UPDATED'
    print(f'  {tag}: {v.sku} | {v.size_label} | R$ {v.price}')

print()
print('=== Resumo final ===')
for v in p.variants.all().order_by('price'):
    print(f'  {v.sku} | {v.size_label} | {v.width_cm}x{v.height_cm}cm | R$ {v.price}')
