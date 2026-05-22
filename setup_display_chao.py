"""Cria o produto Display de Chão (expositor de produtos em papelão)."""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from decimal import Decimal
from apps.catalog.models import Product, ProductVariant, Category

SLUG = 'display-de-chao'
CAT_SLUG = 'totens-pdv'

cat = Category.objects.get(slug=CAT_SLUG)

p, created = Product.objects.update_or_create(
    slug=SLUG,
    defaults=dict(
        category=cat,
        name='Display de Chão',
        short_description=(
            "Display de chão em papelão para expor produtos em pontos "
            "estratégicos do PDV. Vai dobrado para facilitar a montagem e "
            "baratear o frete — montagem automática ou manual."
        ),
        description=(
            "O Display de Chão e Expositores são ideais para expor seus "
            "produtos em pontos estratégicos, destacando-os e favorecendo o "
            "aumento das suas vendas.\n\n"
            "É feito em papelão de altíssima qualidade e impresso "
            "digitalmente em alta resolução. Para facilitar a montagem e "
            "deixar o frete mais barato, ele é entregue dobrado.\n\n"
            "Produzimos com montagem automática (sistema Faster Displays) ou "
            "montagem manual, conforme a necessidade da sua ação.\n\n"
            "Melhore a comunicação da sua marca usando um display de chão "
            "para a exposição de produtos."
        ),
        featured_image=None,  # usuário sobe pelo admin
        is_active=True,
        is_featured=False,
        meta_title='Display de Chão Personalizado para PDV | NGD',
        meta_description=(
            'Display de chão em papelão para exposição de produtos no PDV. '
            'Impressão digital em alta resolução, entregue dobrado, montagem '
            'automática ou manual. Personalizado. Envio para todo o Brasil.'
        ),
    )
)
print(f'{"CREATED" if created else "UPDATED"} Produto: {p.name} (id={p.id})')

# Variantes por porte — preço-base de referência
VARIANTS = [
    dict(sku='NGD-DISPLAY-CHAO-COMPACTO', size_label='Compacto (30x30x120 cm)',
         width_cm=Decimal('30.00'), height_cm=Decimal('120.00'),
         length_cm=Decimal('30.00'), weight_kg=Decimal('1.200'),
         price=Decimal('149.90')),
    dict(sku='NGD-DISPLAY-CHAO-PADRAO', size_label='Padrão (40x35x150 cm)',
         width_cm=Decimal('40.00'), height_cm=Decimal('150.00'),
         length_cm=Decimal('35.00'), weight_kg=Decimal('1.800'),
         price=Decimal('219.90')),
    dict(sku='NGD-DISPLAY-CHAO-GRANDE', size_label='Grande (50x40x180 cm)',
         width_cm=Decimal('50.00'), height_cm=Decimal('180.00'),
         length_cm=Decimal('40.00'), weight_kg=Decimal('2.500'),
         price=Decimal('319.90')),
]

new_skus = {v['sku'] for v in VARIANTS}
old = p.variants.exclude(sku__in=new_skus)
for sku in old.values_list('sku', flat=True):
    print(f'  - removida variante antiga: {sku}')
old.delete()

for data in VARIANTS:
    v, vcreated = ProductVariant.objects.update_or_create(
        product=p, sku=data['sku'],
        defaults={**data, 'is_active': True},
    )
    tag = 'CREATED' if vcreated else 'UPDATED'
    print(f'  {tag}: {v.sku} | {v.size_label} | R$ {v.price}')

print()
print('=== Resumo final ===')
for v in p.variants.all().order_by('price'):
    print(f'  {v.sku} | {v.size_label} | R$ {v.price}')
print()
print(f'URL: /produto/{SLUG}/')
