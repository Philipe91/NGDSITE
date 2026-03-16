import os
import django
from django.core.files import File
from rembg import remove
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

BRAIN = r"C:\Users\Pc Fechamento\.gemini\antigravity\brain\6340af5d-6bd5-4372-958a-dc2d230b36c7"
NEW_IMAGE = os.path.join(BRAIN, "stopper_prateleira_crunchy_angle_1773425842923.png")

try:
    p = Product.objects.get(name='Stopper de Prateleira')
    print(f"Atualizando imagem para: {p.name}...")
    
    with open(NEW_IMAGE, "rb") as f:
        raw_data = f.read()
    
    # Remove background
    clean_data = remove(raw_data)
    
    img_io = io.BytesIO(clean_data)
    p.featured_image.save(f"stopper-de-prateleira-premium.png", File(img_io), save=True)
    print("Imagem do Stopper atualizada com sucesso!")

except Product.DoesNotExist:
    print("Produto 'Stopper de Prateleira' nao encontrado.")
except Exception as e:
    print(f"Erro: {e}")
