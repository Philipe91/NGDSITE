import os
import shutil
import django
from django.core.files import File
from rembg import remove
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product, ProductVariant, Category

BRAIN = r"C:\Users\Pc Fechamento\.gemini\antigravity\brain\6340af5d-6bd5-4372-958a-dc2d230b36c7"
# Caminho da imagem de IA do Totem Eliptico original (2 alterações atrás)
OLD_IMAGE = os.path.join(BRAIN, "totem_eliptico_poliondas_1773421524377.png")

try:
    Product.objects.filter(name__icontains='Totem Triedro').delete()
    print("Totem Triedro deletado.")
    
    cat = Category.objects.filter(slug='ponto-de-venda').first() or Category.objects.first()
    
    p, created = Product.objects.get_or_create(
        name='Totem Elíptico em Poliondas',
        defaults={
            'category': cat,
            'short_description': "Totem Elíptico fabricado(a) em Poliondas, muito mais resistente.",
            'description': "O grande diferencial do Totem Elíptico é a sua fabricação em Poliondas, substituindo o papelão descartável por um material resistente à umidade, durável e com acabamento visual superior para o seu PDV.",
        }
    )
    
    if created:
        print("Totem Elíptico recriado!")
        ProductVariant.objects.create(
            product=p,
            sku=f"NGD-{p.slug[:20].upper()}-001",
            size_label="Tamanho Padrão",
            width_cm=50,
            height_cm=150,
            price=89.90
        )
    
    with open(OLD_IMAGE, "rb") as f:
        raw_data = f.read()
    
    clean_data = remove(raw_data)
    img_io = io.BytesIO(clean_data)
    
    filename = "totem-eliptico-em-poliondas-restaurado.png"
    p.featured_image.save(filename, File(img_io), save=True)
    print("Imagem original do Totem Elíptico restaurada no banco.")
    
    # Atualiza o slider
    static_img_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'NGDSITE', 'static', 'img')
    shutil.copy(p.featured_image.path, os.path.join(static_img_dir, 'totem_ptbr.png'))
    print("Imagem copiada para o slider!")

except Exception as e:
    print(f"Erro: {e}")
