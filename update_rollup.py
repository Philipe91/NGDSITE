import os, django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product, ProductVariant

try:
    p = Product.objects.get(slug='banner-rollup')
    
    # Update description and short description based on user input
    p.short_description = 'Banner Rollup, elegante e moderno, fácil de transportar e montar graças à estrutura em alumínio e ABS.'
    p.description = 'Configure seu Produto com Facilidade! Configure seu produto em poucos passos, escolha o prazo de produção ideal e calcule o frete. Anexe seus arquivos agora ou, se preferir, envie após a compra. Baixe nosso gabarito e manual com instruções para o envio de arquivos. É Indicado para uso interno em eventos, feiras, stands e exposição em PDV reforçando sua marca com estilo!'
    p.save()
    
    # Update variant price
    variant = p.variants.first()
    if variant:
        variant.price = 329.90
        variant.save()
        print('Rollup product and variant updated successfully to R$ 329,90.')
    else:
        print('No variants found for Rollup.')

except Exception as e:
    print('Error:', e)
