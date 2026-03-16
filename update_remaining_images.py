import os
import django
from django.core.files import File
from rembg import remove
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

BRAIN = r"C:\Users\Pc Fechamento\.gemini\antigravity\brain\6340af5d-6bd5-4372-958a-dc2d230b36c7"

updates = {
    'Wobbler de Gôndola':               os.path.join(BRAIN, "wobbler_gondola_poliondas_1773422418095.png"),
    'Stopper de Prateleira':            os.path.join(BRAIN, "stopper_prateleira_poliondas_1773422445369.png"),
    'Faixa de Gôndola (Régua)':         os.path.join(BRAIN, "faixa_gondola_poliondas_1773422471037.png"),
    'Placa de Campo (Poliondas)':       os.path.join(BRAIN, "placa_campo_poliondas_1773422728294.png"),
}

for prod_name, img_path in updates.items():
    try:
        p = Product.objects.get(name=prod_name)
    except Product.DoesNotExist:
        print(f"Produto nao encontrado: {prod_name}, pulando.")
        continue

    print(f"Removendo fundo e salvando imagem para: {prod_name}...")
    with open(img_path, "rb") as f:
        raw = f.read()

    output = remove(raw)
    img_io = io.BytesIO(output)
    p.featured_image.save(f"{p.slug}_ai.png", File(img_io), save=True)
    print(f"  OK: {p.name}")

print("\nTodas as imagens foram atualizadas!")
