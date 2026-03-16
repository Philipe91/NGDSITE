import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

def update_hero_images():
    static_img_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'NGDSITE', 'static', 'img')

    try:
        cubo = Product.objects.get(name='Cubo Promocional em Poliondas')
        if cubo.featured_image:
            shutil.copy(cubo.featured_image.path, os.path.join(static_img_dir, 'cubo_ptbr.png'))
            print("Cubo slider image copied.")
    except Exception as e:
        print("Cubo error:", e)

    try:
        totem = Product.objects.get(name='Totem Elíptico em Poliondas')
        if totem.featured_image:
            shutil.copy(totem.featured_image.path, os.path.join(static_img_dir, 'totem_ptbr.png'))
            print("Totem slider image copied.")
    except Exception as e:
        print("Totem error:", e)

if __name__ == '__main__':
    update_hero_images()
