import os
import django
from django.core.files import File
from rembg import remove
from PIL import Image
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product, Category, ProductVariant

# Define paths for the generated images
input_paths = {
    'Totem Elíptico em Poliondas': r"C:\Users\Pc Fechamento\.gemini\antigravity\brain\6340af5d-6bd5-4372-958a-dc2d230b36c7\totem_eliptico_poliondas_1773421524377.png",
    'Cubo Promocional em Poliondas': r"C:\Users\Pc Fechamento\.gemini\antigravity\brain\6340af5d-6bd5-4372-958a-dc2d230b36c7\cubo_poliondas_1773421466326.png",
    'Lixeira Personalizada em Poliondas': r"C:\Users\Pc Fechamento\.gemini\antigravity\brain\6340af5d-6bd5-4372-958a-dc2d230b36c7\lixeira_poliondas_1773421556683.png"
}

# The names of the products we want to KEEP. Any others will be DELETED.
keep_products = [
    'Totem Elíptico em Poliondas',
    'Cubo Promocional em Poliondas',
    'Wobbler de Gôndola',
    'Stopper de Prateleira',
    'Faixa de Gôndola (Régua)',
    'Banner Rollup',
    'Placa de Campo (Poliondas)',
    'Lixeira Personalizada em Poliondas'
]

# Get the category for testing/creating
cat = Category.objects.filter(slug='ponto-de-venda').first() or Category.objects.first()

def process_and_save_image(product, raw_image_path):
    # Remove background using rembg
    with open(raw_image_path, "rb") as f:
        input_data = f.read()

    print(f"Buscando remover fundo de {product.name}...")
    output_data = remove(input_data)
    
    # Save temporarily to a BytesIO object
    img_io = io.BytesIO(output_data)
    image_name = f"{product.slug}_ai_clean.png"
    
    # Save to product
    product.featured_image.save(image_name, File(img_io), save=True)
    print(f"Imagem atualizada com sucesso para: {product.name}")

# 1. Limpar produtos duplicados / indesejados (Ex. papelão)
all_products = Product.objects.all()
for p in all_products:
    # First, let's normalize names to check against our keep list, 
    # but some exist like "Totem Eleptico Lama" instead of "Totem Elíptico em Poliondas".
    # We will just wipe everything that is NOT strictly in our keep_products exact list.
    if p.name not in keep_products:
        print(f"Removendo produto antigo: {p.name}")
        p.delete()

# 2. Criar ou atualizar os produtos da lista keep_products
for prod_name in keep_products:
    p, created = Product.objects.get_or_create(
        name=prod_name,
        defaults={
            'category': cat,
            'short_description': f"{prod_name} fabricado(a) em material resistente e durável.",
            'description': f"O grande diferencial do {prod_name} é a sua fabricação em Poliondas, que substitui o papelão com excelência. Isso garante durabilidade, leveza, resistência à umidade e um acabamento premium, permitindo uso prolongado mesmo em ambientes com alta circulação.",
        }
    )

    if created:
        print(f"Criado novo produto: {prod_name}")
        import uuid
        ProductVariant.objects.create(
            product=p,
            sku=f"NGD-{p.slug[:20].upper()}-001",
            size_label="Tamanho Padrão",
            width_cm=50,
            height_cm=150 if 'Totem' in prod_name else 80,
            price=89.90 if 'Lixeira' not in prod_name else 149.90
        )
    else:
        # Atualiza descrições para destacar Poliondas sempre
        p.short_description = f"{prod_name} fabricado(a) em Poliondas, muito mais resistente."
        p.description = f"O grande diferencial do {prod_name} é a sua fabricação em Poliondas, substituindo o papelão descartável por um material resistente à umidade, durável e com acabamento visual superior para o seu PDV."
        p.save()

    # Se este produto teve imagem gerada, vamos anexar
    if prod_name in input_paths:
        process_and_save_image(p, input_paths[prod_name])

print("Limpeza do catálogo e atualização de imagens concluídas com sucesso!")
