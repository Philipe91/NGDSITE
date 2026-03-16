import os
import shutil
import django
from django.core.files import File
from rembg import remove
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

BRAIN = r"C:\Users\Pc Fechamento\.gemini\antigravity\brain\6340af5d-6bd5-4372-958a-dc2d230b36c7"
NEW_IMAGE = os.path.join(BRAIN, "media__1773429929530.png")

try:
    p = Product.objects.get(name='Totem Triedro em Poliondas')
    print(f"Atualizando imagem para: {p.name} usando a segunda imagem do usuario...")
    
    with open(NEW_IMAGE, "rb") as f:
        raw_data = f.read()
    
    # Removendo fundo
    clean_data = remove(raw_data)
    
    img_io = io.BytesIO(clean_data)
    filename = "totem-triedro-poliondas-redbull-clean.png"
    p.featured_image.save(filename, File(img_io), save=True)
    print("Imagem nova no BD OK!")
    
    print("Copiando para a pasta static (Home)...")
    static_img_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'NGDSITE', 'static', 'img')
    shutil.copy(p.featured_image.path, os.path.join(static_img_dir, 'totem_triedro.png'))
    print("Imagem do Totem Triedro copiada para o slider da Home (static/img/totem_triedro.png) com sucesso!")

except Product.DoesNotExist:
    print("Produto não encontrado!")
except Exception as e:
    print(f"Erro: {e}")
