"""Cria/atualiza o produto Totem Réplica no DB + vincula ao card do megamenu.
Totem Réplica = totem com recorte especial (faca de contorno) que reproduz
pessoa, personagem ou produto em tamanho real. Produto personalizado."""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from decimal import Decimal
from apps.catalog.models import Product, ProductVariant, Category, MegaMenuTotensCard

SLUG = 'totem-replica-em-poliondas'
CAT_SLUG = 'totens-pdv'

cat = Category.objects.get(slug=CAT_SLUG)

p, created = Product.objects.update_or_create(
    slug=SLUG,
    defaults=dict(
        category=cat,
        name='Totem Réplica em Poliondas',
        short_description=(
            "Totem com recorte especial (faca de contorno) que reproduz uma "
            "pessoa, personagem ou produto em tamanho real. Em poliondas 3mm, "
            "com base dobrável — impacto visual imediato no PDV."
        ),
        description=(
            "O Totem Réplica NGD é uma peça publicitária de recorte especial: "
            "o contorno é cortado em faca para reproduzir fielmente a silhueta "
            "de uma pessoa, personagem, mascote ou produto. Fabricado em "
            "polipropileno corrugado (poliondas) de 3mm, com impressão UV em "
            "alta resolução.\n\n"
            "Acompanha base acoplada na parte de trás — dobrável e removível "
            "para facilitar transporte e armazenamento. Montado, a base fica "
            "escondida e o totem fica em pé sozinho.\n\n"
            "É o recurso ideal para clonar influenciadores e garotos-propaganda "
            "no ponto de venda, criar cenários para eventos (aniversários, "
            "casamentos, formaturas), ativar marcas em feiras e stands, ou dar "
            "vida a mascotes e personagens.\n\n"
            "Por ser um produto 100% personalizado — o formato do recorte "
            "depende da imagem enviada — o valor final é definido por "
            "orçamento. As faixas de altura abaixo servem como referência "
            "de partida."
        ),
        featured_image=None,  # usuário sobe pelo admin
        is_active=True,
        is_featured=False,
        meta_title='Totem Réplica (Recorte Especial) em Poliondas | NGD',
        meta_description=(
            'Totem com recorte de faca de contorno: replica pessoa, personagem '
            'ou produto em tamanho real. Poliondas 3mm, base dobrável, '
            'impressão UV. Personalizado sob orçamento. Envio para todo Brasil.'
        ),
    )
)
print(f'{"CREATED" if created else "UPDATED"} Produto: {p.name} (id={p.id})')

# Variantes por faixa de altura — preço-base de referência (produto é cotado)
VARIANTS = [
    dict(sku='NGD-TOTEM-REPLICA-P', size_label='Pequeno (até 1,00 m)',
         width_cm=Decimal('60.00'), height_cm=Decimal('100.00'),
         length_cm=Decimal('30.00'), weight_kg=Decimal('0.700'),
         price=Decimal('119.90')),
    dict(sku='NGD-TOTEM-REPLICA-M', size_label='Médio (1,01 a 1,50 m)',
         width_cm=Decimal('70.00'), height_cm=Decimal('150.00'),
         length_cm=Decimal('35.00'), weight_kg=Decimal('1.100'),
         price=Decimal('179.90')),
    dict(sku='NGD-TOTEM-REPLICA-G', size_label='Tamanho Real (1,51 a 2,00 m)',
         width_cm=Decimal('80.00'), height_cm=Decimal('200.00'),
         length_cm=Decimal('40.00'), weight_kg=Decimal('1.700'),
         price=Decimal('249.90')),
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

# Vincula o card #5 do megamenu ao produto e remove badge "em_breve"
print()
print('=== Atualizando card do megamenu (#5 Totem Réplica) ===')
try:
    card = MegaMenuTotensCard.objects.get(order=5)
    card.product = p
    card.badge = ''  # remove em_breve -> sai do cinza, mostra Comprar
    card.is_active = True
    card.save()
    print(f'  OK card #{card.order} vinculado ao produto, badge limpa')
except MegaMenuTotensCard.DoesNotExist:
    print('  ALERTA: card #5 nao encontrado')

print()
print('=== Resumo final ===')
for v in p.variants.all().order_by('price'):
    print(f'  {v.sku} | {v.size_label} | R$ {v.price}')
