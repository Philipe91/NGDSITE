import os, sys, django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Category, Product, ProductVariant

# Define categories
extra_cats = ['Cubo Promocional', 'Wobbler', 'Stopper', 'Faixa de Gondola', 'Rollup']

products_data = [
    {
        'category': 'Cubo Promocional',
        'name': 'Cubo Promocional em Poliondas',
        'short_desc': 'Cubo interativo e empilhavel para displays e vitrines.',
        'desc': 'Ideal para formar vitrines criativas. O Cubo Promocional e leve, facil de montar e permite empilhamento, criando layouts dinamicos para sua marca.',
        'sku': 'CB-PROM-001',
        'price': 45.90
    },
    {
        'category': 'Wobbler',
        'name': 'Wobbler de Gondola',
        'short_desc': 'Destaque seus produtos direto na prateleira com movimento.',
        'desc': 'Peca promocional fixada nas prateleiras que se destaca visualmente devido a haste flexivel, chamando atencao imediata do consumidor no ponto de venda.',
        'sku': 'WB-GOND-001',
        'price': 3.50
    },
    {
        'category': 'Stopper',
        'name': 'Stopper de Prateleira',
        'short_desc': 'Bloqueio visual para destacar categorias ou promocoes.',
        'desc': 'O Stopper e fixado perpendicularmente a prateleira, sobressaindo para o corredor. Excelente para delimitar o espaco da sua marca e informar campanhas.',
        'sku': 'STP-PRAT-001',
        'price': 12.90
    },
    {
        'category': 'Faixa de Gondola',
        'name': 'Faixa de Gondola (Regua)',
        'short_desc': 'Organize e decore as prateleiras do seu PDV.',
        'desc': 'A Faixa de Gondola ou Regua e aplicada na borda das prateleiras, perfeita para informar precos de forma padronizada ou expandir o branding do produto.',
        'sku': 'FX-GOND-001',
        'price': 5.80
    },
    {
        'category': 'Rollup',
        'name': 'Banner Rollup',
        'short_desc': 'O expositor mais versatil e portatil para seus eventos.',
        'desc': 'O Banner Rollup possui uma estrutura de aluminio elegante e sistema de recolhimento automatico da lona. E ideal para eventos, feiras e pontos de venda itinerantes devido a sua facilidade de montagem e transporte. Acompanha bolsa.',
        'sku': 'RU-BANN-80X200',
        'price': 189.90
    }
]

for cat_name in extra_cats:
    Category.objects.get_or_create(name=cat_name, defaults={'slug': slugify(cat_name)})

for pd in products_data:
    cat = Category.objects.get(name=pd['category'])
    prod, created = Product.objects.update_or_create(
        slug=slugify(pd['name']),
        defaults={
            'name': pd['name'],
            'category': cat,
            'short_description': pd['short_desc'],
            'description': pd['desc'],
            'is_active': True,
        }
    )
    
    ProductVariant.objects.get_or_create(
        sku=pd['sku'],
        defaults={
            'product': prod,
            'size_label': 'Padrao',
            'width_cm': 10.00,
            'height_cm': 10.00,
            'price': pd['price']
        }
    )
    print(f"Ready: {pd['name']}")

print('DONE SEEDING EXTRA')
