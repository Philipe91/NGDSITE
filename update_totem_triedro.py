"""Atualiza dados do produto Totem Triedro com base nas informações do mercado."""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from decimal import Decimal
from apps.catalog.models import Product, ProductVariant

SLUG = 'totem-triedro-em-poliondas'

p = Product.objects.get(slug=SLUG)

p.short_description = (
    "Totem publicitário vertical em formato triangular com comunicação 360° "
    "nas três faces. Em poliondas 3mm, vem cortado, vincado e pronto para uso — "
    "sem montagem complicada."
)

p.description = (
    "O Totem Triedro NGD é uma peça publicitária triangular fabricada em "
    "polipropileno corrugado (poliondas) de 3mm. Com três faces "
    "personalizáveis, entrega comunicação 360° em qualquer ambiente: PDV, "
    "eventos, feiras, halls de entrada, lojas e shoppings.\n\n"
    "Impresso em alta resolução com tecnologia UV de cura a frio — cores "
    "vivas, durabilidade superior e sem odor químico. Chega pronto para uso, "
    "já cortado e vincado, sem suportes ou ferramentas para montar. É só "
    "posicionar no chão e o totem fica em pé sozinho.\n\n"
    "Ideal para destacar ofertas no ponto de venda, lançamentos de produto, "
    "ações em eventos e sinalização em múltiplos pontos do ambiente. "
    "Tamanhos disponíveis: 40×120, 40×190 e 60×190 cm."
)

p.meta_title = "Totem Triedro em Poliondas Personalizado | NGD"
p.meta_description = (
    "Totem publicitário triangular com comunicação 360° em poliondas 3mm. "
    "Tamanhos 40x120, 40x190 e 60x190 cm. Impressão UV em alta resolução. "
    "Envio para todo o Brasil."
)
p.save()
print(f'OK Produto atualizado: {p.name}')

# Variantes: 3 tamanhos (40x120, 40x190, 60x190) — preços crescentes
VARIANTS = [
    dict(sku='NGD-TOTEM-TRIEDRO-40X120', size_label='40x120 cm',
         width_cm=Decimal('40.00'), height_cm=Decimal('120.00'),
         length_cm=Decimal('40.00'), weight_kg=Decimal('0.900'),
         price=Decimal('129.90')),
    dict(sku='NGD-TOTEM-TRIEDRO-40X190', size_label='40x190 cm',
         width_cm=Decimal('40.00'), height_cm=Decimal('190.00'),
         length_cm=Decimal('40.00'), weight_kg=Decimal('1.400'),
         price=Decimal('169.90')),
    dict(sku='NGD-TOTEM-TRIEDRO-60X190', size_label='60x190 cm',
         width_cm=Decimal('60.00'), height_cm=Decimal('190.00'),
         length_cm=Decimal('60.00'), weight_kg=Decimal('2.000'),
         price=Decimal('219.90')),
]

# Deleta variantes antigas que não casam com os novos SKUs
new_skus = {v['sku'] for v in VARIANTS}
old = p.variants.exclude(sku__in=new_skus)
removed = list(old.values_list('sku', flat=True))
old.delete()
for sku in removed:
    print(f'  - removida variante antiga: {sku}')

# Cria/atualiza as 3 variantes corretas
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
    print(f'  {v.sku} | {v.size_label} | {v.width_cm}x{v.height_cm}cm | {v.weight_kg}kg | R$ {v.price}')
