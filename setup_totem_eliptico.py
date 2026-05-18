"""Cria/atualiza o produto Totem Elíptico no DB + vincula ao card do megamenu.
Remove o badge 'em_breve' pra sair do estado cinza no dropdown."""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from decimal import Decimal
from apps.catalog.models import Product, ProductVariant, Category, MegaMenuTotensCard

SLUG = 'totem-eliptico-em-poliondas'
CAT_SLUG = 'totens-pdv'

cat = Category.objects.get(slug=CAT_SLUG)

p, created = Product.objects.update_or_create(
    slug=SLUG,
    defaults=dict(
        category=cat,
        name='Totem Elíptico em Poliondas',
        short_description=(
            "Totem publicitário curvado em formato elíptico, com duas faces "
            "personalizáveis. Em poliondas 3mm, vai cortado, vincado e pronto "
            "para uso — visual elegante e fácil montagem."
        ),
        description=(
            "O Totem Elíptico NGD é uma peça publicitária vertical de formato "
            "curvado/oval, fabricada em polipropileno corrugado (poliondas) de "
            "3mm. Com duas faces personalizáveis, entrega comunicação dupla com "
            "presença visual sofisticada — ideal para PDV premium, halls de "
            "entrada de lojas, eventos corporativos e ações de marketing.\n\n"
            "Impresso em alta resolução com tecnologia UV de cura a frio — "
            "cores vivas, durabilidade superior e sem odor químico. Chega "
            "pronto para uso, já cortado e vincado, sem suportes ou "
            "ferramentas para montar. Posiciona direto no chão.\n\n"
            "Tamanhos disponíveis: 50×150, 60×160 e 60×180 cm (face única)."
        ),
        featured_image=None,  # user vai fazer upload pelo admin
        is_active=True,
        is_featured=False,
        meta_title='Totem Elíptico em Poliondas Personalizado | NGD',
        meta_description=(
            'Totem publicitário curvado com 2 faces em poliondas 3mm. '
            'Tamanhos 50x150, 60x160 e 60x180 cm. Impressão UV em alta '
            'resolução. Envio para todo Brasil.'
        ),
    )
)
print(f'{"CREATED" if created else "UPDATED"} Produto: {p.name} (id={p.id})')

VARIANTS = [
    dict(sku='NGD-TOTEM-ELIPTICO-50X150', size_label='50x150 cm',
         width_cm=Decimal('50.00'), height_cm=Decimal('150.00'),
         length_cm=Decimal('40.00'), weight_kg=Decimal('1.000'),
         price=Decimal('99.90')),
    dict(sku='NGD-TOTEM-ELIPTICO-60X160', size_label='60x160 cm',
         width_cm=Decimal('60.00'), height_cm=Decimal('160.00'),
         length_cm=Decimal('45.00'), weight_kg=Decimal('1.300'),
         price=Decimal('129.90')),
    dict(sku='NGD-TOTEM-ELIPTICO-60X180', size_label='60x180 cm',
         width_cm=Decimal('60.00'), height_cm=Decimal('180.00'),
         length_cm=Decimal('45.00'), weight_kg=Decimal('1.600'),
         price=Decimal('159.90')),
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

# Atualiza o card do megamenu: tira badge "em_breve" e vincula ao produto
print()
print('=== Atualizando card do megamenu ===')
card = MegaMenuTotensCard.objects.filter(title__icontains='liptico').first()
if card:
    card.product = p
    card.badge = ''  # remove "em_breve" → sai do cinza, mostra botão Comprar
    card.is_active = True
    card.save()
    print(f'  OK Card #{card.order} vinculado ao produto, badge limpa')
else:
    print('  ALERTA: card do menu nao encontrado')

print()
print('=== Resumo final do produto ===')
for v in p.variants.all().order_by('price'):
    print(f'  {v.sku} | {v.size_label} | R$ {v.price}')
