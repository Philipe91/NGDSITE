"""Corrige o Totem Elíptico: material real é Papel Duplex Matte 350g
(não poliondas). Ajusta nome, descrição, specs e meta — mantendo a voz NGD.
Slug mantido (totem-eliptico-em-poliondas) pra não quebrar links/hero."""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

p = Product.objects.get(slug='totem-eliptico-em-poliondas')

# Título: só "Totem Elíptico"
p.name = 'Totem Elíptico'

p.short_description = (
    "Totem publicitário vertical em formato elíptico, com 2 faces "
    "personalizadas em 4×4 cores. Em Papel Duplex Matte 350g com corte "
    "reto — visual elegante e moderno pra destacar sua marca no PDV."
)

p.description = (
    "O Totem Elíptico NGD é uma peça publicitária vertical de formato "
    "curvado/oval, com 2 faces totalmente personalizáveis. Design "
    "atrativo e elegante que se destaca em qualquer ambiente, com altura "
    "pensada pra boa visibilidade e ótima otimização de espaço.\n\n"
    "Ficha técnica:\n"
    "• Material: Papel Duplex Matte 350g — rígido, acabamento fosco "
    "premium e cores fiéis.\n"
    "• Cores: 4×4 (impressão colorida na frente e no verso).\n"
    "• Acabamento: corte reto de precisão.\n\n"
    "Versátil pra diferentes áreas — PDV, lojas, halls de entrada, "
    "eventos corporativos e ações de marketing. Comunicação dupla com "
    "presença visual sofisticada, ideal pra alcançar mais clientes em "
    "espaços com circulação.\n\n"
    "Tamanhos disponíveis: 50×150, 60×160 e 60×180 cm."
)

p.meta_title = "Totem Elíptico Personalizado | NGD"
p.meta_description = (
    "Totem elíptico publicitário com 2 faces em Papel Duplex Matte 350g, "
    "impressão 4×4 cores e corte reto. Tamanhos 50x150, 60x160 e 60x180 cm. "
    "Envio para todo o Brasil."
)
p.save()
print(f'OK Produto atualizado: {p.name!r}')
print(f'  short_desc: {len(p.short_description)} chars')
print(f'  description: {len(p.description)} chars')
print(f'  meta_title:  {p.meta_title}')
print()
print('=== Variantes (preservadas) ===')
for v in p.variants.all().order_by('price'):
    print(f'  {v.sku} | {v.size_label} | R$ {v.price}')
