import os, sys, django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

# Map product ID to the original image path they had before today
media_dir = r"c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured"

original_images = {
    1:  "totem_eliptico_mock.png",          # Totem Elíptico (Lamá) - original mock
    2:  "cubo_promocional_mock.png",        # Cubo Promocional - original mock
    3:  "wobbler_mock.png",                 # Wobbler Promocional - original mock
    4:  "totem-triangular.png",             # Totem Triangular
    5:  "totem-cubo.png",                   # Totem Cubo
    6:  "totem-triedro.png",                # Totem Triedro
    7:  "totem_eliptico_1773089611128.png", # Totem Elíptico (Lamá) v2
    8:  "totem-banana.png",                 # Totem Banana
    9:  "totem-replica.png",                # Totem Replica
    10: "totem-eleptico-lama.png",          # Totem Eléptico Lama
    11: "cubo_promocional_1773089627220.png", # Cubo Promocional em Poliondas
    12: "wobbler_gondola_1773089646179.png",  # Wobbler de Gondola
    13: "stopper_prateleira_1773089664009.png", # Stopper de Prateleira
    14: "faixa_gondola_1773089535045.png",    # Faixa de Gondola
    15: "banner_rollup_1773089680554.png",    # Banner Rollup
}

for pid, img_name in original_images.items():
    img_path = os.path.join(media_dir, img_name)
    if not os.path.exists(img_path):
        print(f"  [SKIP] ID {pid}: image not found -> {img_name}")
        continue
    try:
        p = Product.objects.get(id=pid)
        with open(img_path, 'rb') as f:
            p.featured_image.save(img_name, File(f), save=True)
        print(f"  [OK] {p.name} -> {img_name}")
    except Product.DoesNotExist:
        print(f"  [SKIP] Product ID {pid} not found in DB")

print("\nImagens restauradas com sucesso!")
