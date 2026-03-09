import os, sys, django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product
from django.core.files import File

# Paths to the AI-generated images
artifacts_dir = r"C:\Users\Pc Fechamento\.gemini\antigravity\brain\cc5331ee-3c14-447e-86a0-2f0c20583ea4"
images_map = {
    'totem-triangular': 'totem_triangular_1773084027121.png',
    'totem-cubo': 'totem_cubo_1773084111920.png',
    'totem-triedro': 'totem_triedro_1773084143016.png',
    'totem-eleptico-lama': 'totem_eliptico_1773084156844.png',
    'totem-banana': 'totem_banana_1773084191788.png',
    'totem-replica': 'totem_replica_1773084217078.png',
}

media_dest_dir = r"C:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured"
os.makedirs(media_dest_dir, exist_ok=True)

for slug, filename in images_map.items():
    src_path = os.path.join(artifacts_dir, filename)
    if not os.path.exists(src_path):
        print(f"Skipping {slug}, image not found at {src_path}")
        continue
        
    try:
        product = Product.objects.get(slug=slug)
        filename_only = f"{slug}.png"
        
        # Save exact path to django
        with open(src_path, 'rb') as f:
            product.featured_image.save(filename_only, File(f), save=True)
            
        print(f"Attached image to {product.name}")
    except Product.DoesNotExist:
        print(f"Product {slug} does not exist.")
        
print("DONE ATTACHING IMAGES")
