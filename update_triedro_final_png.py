import os
import shutil
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Imagem enviada pelo usuario sem fundo já tratada
NEW_IMAGE = os.path.join(BASE_DIR, "triedo.png")

print(f"Buscando a imagem: {NEW_IMAGE}")
if not os.path.exists(NEW_IMAGE):
    print("ERRO: O arquivo triedo.png nao foi encontrado na pasta NGDSITE! Tem certeza que ele ja foi salvo ai?")
else:
    try:
        p = Product.objects.get(name='Totem Triedro em Poliondas')
        
        with open(NEW_IMAGE, "rb") as f:
            p.featured_image.save("totem-triedro-poliondas-oficial.png", File(f), save=True)
            
        print("Imagem adicionada ao produto no banco de dados!")
        
        # Colocando no slider
        static_img_dir = os.path.join(BASE_DIR, 'static', 'img')
        shutil.copy(p.featured_image.path, os.path.join(static_img_dir, 'totem_triedro.png'))
        print("Imagem copiada para a pasta static do slider (static/img/totem_triedro.png)!")
        
    except Product.DoesNotExist:
        print("Erro: Produto Totem Triedro nao encontrado. O banco de dados foi mexido?")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
