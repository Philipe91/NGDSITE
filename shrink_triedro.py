import os
from PIL import Image

def pad_image(path):
    # Verifica se a imagem existe
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
        
    img = Image.open(path).convert("RGBA")
    width, height = img.size
    
    # Criar um novo canvas 1.4x maior (para reduzir a imagem atual em ~30% quando exibida em object-contain)
    new_width = int(width * 1.4)
    new_height = int(height * 1.4)
    
    new_img = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    x = (new_width - width) // 2
    y = (new_height - height) // 2
    
    new_img.paste(img, (x, y), img)
    new_img.save(path)
    print(f"Padding added to {path}")

# Caminho no static
static_path = r"C:\Users\Pc Fechamento\Documents\NGDSITE\static\img\totem_triedro.png"
pad_image(static_path)

# Vamos achar também no media para manter sincronizado, caso o usuário acesse o produto
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
from apps.catalog.models import Product

try:
    p = Product.objects.get(name='Totem Triedro em Poliondas')
    if p.featured_image:
        pad_image(p.featured_image.path)
except Exception as e:
    print("Erro no DB:", e)
