import os
import django
from django.core.files import File
from rembg import remove
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product, ProductVariant, Category

BRAIN = r"C:\Users\Pc Fechamento\.gemini\antigravity\brain\6340af5d-6bd5-4372-958a-dc2d230b36c7"
# Usando a imagem que o usuário fez upload
NEW_IMAGE = os.path.join(BRAIN, "media__1773428161788.png")

try:
    cat = Category.objects.filter(slug='ponto-de-venda').first() or Category.objects.first()
    
    # Cria o Totem Triedro de volta
    p, created = Product.objects.get_or_create(
        name='Totem Triedro em Poliondas',
        defaults={
            'category': cat,
            'short_description': f"Totem Triedro fabricado em material resistente e durável.",
            'description': f"O grande diferencial do Totem Triedro é a sua fabricação em Poliondas, que substitui o papelão com excelência. Visão 360 graus em formato triangular.",
        }
    )
    
    if created:
        print("Criado novo produto: Totem Triedro")
        ProductVariant.objects.create(
            product=p,
            sku=f"NGD-{p.slug[:20].upper()}-001",
            size_label="Tamanho Padrão",
            width_cm=50,
            height_cm=150,
            price=129.90
        )
    
    print(f"Atualizando imagem para: {p.name} usando imagem do usuario...")
    
    with open(NEW_IMAGE, "rb") as f:
        raw_data = f.read()
    
    # Remove fundo da propria imagem real do usuario já que a de IA deu limite
    clean_data = remove(raw_data)
    
    img_io = io.BytesIO(clean_data)
    p.featured_image.save(f"totem-triedro-poliondas-real.png", File(img_io), save=True)
    print("Imagem do Totem Triedro atualizada com sucesso!")

except Exception as e:
    print(f"Erro: {e}")
