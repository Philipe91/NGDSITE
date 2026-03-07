from django.core.management.base import BaseCommand
from apps.catalog.models import Category, Product, ProductVariant
# from apps.pages.models import Banner, SitePage
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Populate the database with initial Seed Data using Generated Mocks'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando o Seed do Banco de Dados com Novas Imagens...')

        # Caminho base para onde o copy_images_no_shell.py moveu as coisas
        media_dev_dir = r"E:\NGDSITE\media\produtos_mock"

        # 1. CATEGORIAS DE MOCK
        cat_totens, _ = Category.objects.get_or_create(name='Totens PDV', slug='totens-pdv', is_active=True)
        cat_displays, _ = Category.objects.get_or_create(name='Displays / PDV', slug='displays-pdv', is_active=True)

        # 2. PRODUTOS DE MOCK (TOTEM)
        prod_eliptico, _ = Product.objects.get_or_create(
            category=cat_totens,
            name='Totem Elíptico (Lamá)',
            slug='totem-eliptico',
            short_description='Totem Elíptico disponível em diversos formatos. Impressão de alta resolução com cura UV, colorida frente.',
            description='Marketing Inteligente para PDV! Montagem em 3 segundos automontável.',
            is_featured=True
        )
        # Atualizar a imagem
        img_totem_path = os.path.join(media_dev_dir, 'totem_eliptico.png')
        if os.path.exists(img_totem_path) and not prod_eliptico.featured_image:
            with open(img_totem_path, 'rb') as f:
                prod_eliptico.featured_image.save('totem_eliptico_mock.png', File(f), save=True)

        # 3. PRODUTOS DE MOCK (CUBO)
        prod_cubo, _ = Product.objects.get_or_create(
            category=cat_displays,
            name='Cubo Promocional',
            slug='cubo-promocional',
            short_description='Gere volume e chame atenção à distância. Caixas leves e resistentes para montagem de incríveis composições.',
            description='Produzido no poliondas, empilháveis entre si gerando ilhas magníficas de impacto.',
            is_featured=True
        )
        img_cubo_path = os.path.join(media_dev_dir, 'cubo_promocional.png')
        if os.path.exists(img_cubo_path) and not prod_cubo.featured_image:
             with open(img_cubo_path, 'rb') as f:
                prod_cubo.featured_image.save('cubo_promocional_mock.png', File(f), save=True)

        # 4. PRODUTOS DE MOCK (WOBBLER)
        prod_wobbler, _ = Product.objects.get_or_create(
            category=cat_displays,
            name='Wobbler Promocional',
            slug='wobbler',
            short_description='Material que salta aos olhos do cliente, ideal para anunciar lançamentos na gôndola.',
            description='Impresso em alta resolução com formato especial e haste flexível transparente de fixação rápida.',
            is_featured=True
        )
        img_wobbler_path = os.path.join(media_dev_dir, 'wobbler_gondola.png')
        if os.path.exists(img_wobbler_path) and not prod_wobbler.featured_image:
             with open(img_wobbler_path, 'rb') as f:
                prod_wobbler.featured_image.save('wobbler_mock.png', File(f), save=True)


        # 5. VARIANTES DE PRODUTOS
        if not ProductVariant.objects.filter(sku='ELI-40X120').exists():
            ProductVariant.objects.create(product=prod_eliptico, sku='ELI-40X120', size_label='40x120cm', width_cm=40, height_cm=120, price=89.90)
            ProductVariant.objects.create(product=prod_eliptico, sku='ELI-50X150', size_label='50x150cm', width_cm=50, height_cm=150, price=139.90)
            ProductVariant.objects.create(product=prod_eliptico, sku='ELI-60X180', size_label='60x180cm', width_cm=60, height_cm=180, price=179.90)

        if not ProductVariant.objects.filter(sku='CUB-40X40').exists():
            ProductVariant.objects.create(product=prod_cubo, sku='CUB-40X40', size_label='40x40x40cm', width_cm=40, height_cm=40, price=45.00)
        
        if not ProductVariant.objects.filter(sku='WOB-15X15').exists():
            ProductVariant.objects.create(product=prod_wobbler, sku='WOB-15X15', size_label='15x15cm', width_cm=15, height_cm=15, price=4.50)

        # Remake Banner ignorado se os modelos antigos prevalecerem.
        self.stdout.write(self.style.SUCCESS('Seed Finalizado! DB Popular com Imagens PT-BR.'))
