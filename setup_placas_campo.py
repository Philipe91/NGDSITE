import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Category, Product, ProductVariant

def create_placa_de_campo():
    category, _ = Category.objects.get_or_create(
        name="Placas e Sinalização",
        defaults={
            "description": "Placas de sinalização para diversos fins, incluindo lavoura e uso interno.",
        }
    )

    desc_html = """
<p class="text-lg text-gray-700 leading-relaxed mb-6">Produzimos <strong>Placas de Poliondas</strong> para sinalização avançada de plantações e lavouras, oferecendo um acabamento técnico superior que resiste às condições mais extremas do campo.</p>

<p class="mb-6">Diferente de serviços de impressão comuns, somos uma <strong>Indústria de Sinalização Agrícola</strong>. Fabricamos nossas placas seguindo padrões técnicos rigorosos, garantindo total conformidade legal e a máxima durabilidade exigida pelo agronegócio.</p>

<h3 class="font-bold text-xl mt-8 mb-4 border-b pb-2">Diferenciais da Nossa Indústria</h3>
<ul class="list-disc pl-5 space-y-3 mb-8">
  <li>Faturamento exclusivo como insumo industrial (CNAE de Fabricação)</li>
  <li>Itens faturados com os respectivos códigos NCM corretos</li>
  <li>Total conformidade com a <strong>Lei 10.711/2003</strong> (Sistema Nacional de Sementes e Mudas)</li>
  <li>Produzida em Poliondas virgem de 3mm ou 4mm com tratamento especial</li>
</ul>

<h3 class="font-bold text-xl mt-8 mb-4 border-b pb-2">Tecnologia de Produção e Acabamento</h3>
<p class="mb-4">Empregamos tecnologia de ponta com <strong>Impressão Digital UV de Alta Resolução</strong> conjugada a <strong>Corte Oscilante de Alta Precisão</strong>. O resultado? Padronização impecável, encaixes estruturais perfeitos e um resultado visual impressionante, mesmo rodando milhares de unidades simultaneamente.</p>

<ul class="list-disc pl-5 space-y-3 mb-8">
  <li><strong>Impressão UV Direta na Chapa:</strong> Definição incomparável, cores extremamente vibrantes e aderência química total ao substrato.</li>
  <li><strong>Resistência Extrema:</strong> Processo 100% blindado contra água, sol escaldante, e à degradação natural por raios UV e defensivos agrícolas.</li>
</ul>

<div class="bg-primary/5 border border-primary/20 rounded-xl p-6 mt-6">
    <p class="text-primary font-bold text-lg text-center">Aumente o peso e a autoridade da sua marca na lavoura com nossas soluções estruturadas!</p>
</div>
"""

    product, created = Product.objects.get_or_create(
        name="Placa de Campo (Poliondas)",
        defaults={
            "category": category,
            "short_description": "Placas de campo e lavoura de poliondas com conformidade à Lei 10.711/2003. Corte preciso e impressão UV.",
            "description": desc_html,
            "is_active": True,
            "is_featured": True
        }
    )

    if not created:
        product.description = desc_html
        product.save()

    # Create Variants
    sizes = [
        {"size": "30x40 cm", "sku": "PLC-30X40", "p": "39.90", "w": 30, "h": 40, "peso": 0.3, "len": 1},
        {"size": "40x60 cm", "sku": "PLC-40X60", "p": "59.90", "w": 40, "h": 60, "peso": 0.6, "len": 1},
        {"size": "80x100 cm", "sku": "PLC-80X100", "p": "99.90", "w": 80, "h": 100, "peso": 1.5, "len": 1},
    ]

    for s in sizes:
        ProductVariant.objects.get_or_create(
            product=product,
            sku=s['sku'],
            defaults={
                "size_label": s['size'],
                "price": Decimal(s['p']),
                "width_cm": s['w'],
                "height_cm": s['h'],
                "weight_kg": s['peso'],
                "length_cm": s['len'],
            }
        )

    print("Produto Placa de de Campo criado com sucesso!")

if __name__ == "__main__":
    create_placa_de_campo()
