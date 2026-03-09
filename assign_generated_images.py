import os, django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

image_mapping = {
    'faixa-de-gondola-regua': r'C:\Users\Pc Fechamento\.gemini\antigravity\brain\ac567621-7414-4821-b4f1-85f349322df2\faixa_gondola_1773089535045.png',
    'totem-eliptico-lama': r'C:\Users\Pc Fechamento\.gemini\antigravity\brain\ac567621-7414-4821-b4f1-85f349322df2\totem_eliptico_1773089611128.png',
    'cubo-promocional-em-poliondas': r'C:\Users\Pc Fechamento\.gemini\antigravity\brain\ac567621-7414-4821-b4f1-85f349322df2\cubo_promocional_1773089627220.png',
    'wobbler-de-gondola': r'C:\Users\Pc Fechamento\.gemini\antigravity\brain\ac567621-7414-4821-b4f1-85f349322df2\wobbler_gondola_1773089646179.png',
    'stopper-de-prateleira': r'C:\Users\Pc Fechamento\.gemini\antigravity\brain\ac567621-7414-4821-b4f1-85f349322df2\stopper_prateleira_1773089664009.png',
    'banner-rollup': r'C:\Users\Pc Fechamento\.gemini\antigravity\brain\ac567621-7414-4821-b4f1-85f349322df2\banner_rollup_1773089680554.png'
}

for slug, img_path in image_mapping.items():
    try:
        product = Product.objects.get(slug=slug)
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                product.featured_image.save(os.path.basename(img_path), File(f), save=True)
            print(f"Successfully attached image to {product.name}")
        else:
            print(f"Image not found at {img_path}")
    except Product.DoesNotExist:
        print(f"Product with slug {slug} not found.")
    except Exception as e:
        print(f"Error processing {slug}: {e}")

print("Done.")
