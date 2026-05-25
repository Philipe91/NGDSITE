"""Atualiza dados do produto Lixeira Personalizada em Poliondas — descrição
rica + 3 variantes por porte. Alinhado com a linha de poliondas da NGD."""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from decimal import Decimal
from apps.catalog.models import Product, ProductVariant

SLUG = 'lixeira-personalizada-em-poliondas'

p = Product.objects.get(slug=SLUG)
p.name = 'Lixeira Personalizada em Poliondas'

p.short_description = (
    "Lixeira ecológica personalizada em poliondas para PDV, eventos e "
    "ambientes corporativos. Material resistente à umidade, impressão UV "
    "nas faces externas — vai dobrada, monta em segundos."
)

p.description = (
    "A Lixeira Personalizada NGD é fabricada em polipropileno corrugado "
    "(poliondas) de 3 mm — o mesmo material premium dos nossos totens e "
    "displays. Substitui as lixeiras de papelão com folga: resiste à "
    "umidade, é mais durável e mantém o acabamento mesmo em ambientes "
    "de alta circulação.\n\n"
    "Recebe impressão UV em alta resolução nas 4 faces externas, "
    "permitindo branding completo da sua marca, sinalização de descarte "
    "seletivo ou comunicação de campanha. As cores não desbotam com o "
    "tempo e a tinta não tem cheiro químico — ideal para uso indoor.\n\n"
    "Vem dobrada de fábrica e é montada em poucos segundos, sem "
    "ferramentas. Quando precisar guardar, dobra de volta e ocupa pouco "
    "espaço no estoque. Encaixa em sacos plásticos comerciais padrão.\n\n"
    "Disponível em 3 portes: pequena (30 L), média (50 L) e grande "
    "(80 L) — escolha conforme o fluxo de descarte do seu ambiente."
)

p.meta_title = "Lixeira Personalizada em Poliondas para PDV | NGD"
p.meta_description = (
    "Lixeira ecológica personalizada em poliondas 3mm com impressão UV "
    "nas 4 faces. Tamanhos 30L, 50L e 80L. Resistente à umidade, vai "
    "dobrada. Envio para todo o Brasil."
)
p.is_active = True
p.save()
print(f'OK Produto atualizado: {p.name}')

# 3 variantes por porte/capacidade
VARIANTS = [
    dict(sku='NGD-LIXEIRA-PDV-P30', size_label='Pequena · 30 L (30×30×50 cm)',
         width_cm=Decimal('30.00'), length_cm=Decimal('30.00'),
         height_cm=Decimal('50.00'), weight_kg=Decimal('0.700'),
         price=Decimal('99.90')),
    dict(sku='NGD-LIXEIRA-PDV-M50', size_label='Média · 50 L (35×35×60 cm)',
         width_cm=Decimal('35.00'), length_cm=Decimal('35.00'),
         height_cm=Decimal('60.00'), weight_kg=Decimal('1.000'),
         price=Decimal('149.90')),
    dict(sku='NGD-LIXEIRA-PDV-G80', size_label='Grande · 80 L (40×40×70 cm)',
         width_cm=Decimal('40.00'), length_cm=Decimal('40.00'),
         height_cm=Decimal('70.00'), weight_kg=Decimal('1.400'),
         price=Decimal('199.90')),
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
    print(f'  {v.sku} | {v.size_label} | R$ {v.price}')
print()
print(f'URL: /produto/{SLUG}/')
