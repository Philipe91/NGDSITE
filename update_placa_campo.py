"""Polimento da página da Placa de Campo Poliondas:
descrição rica + meta SEO + variantes preservadas."""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

p = Product.objects.get(slug='placa-de-campo-poliondas')
p.name = 'Placa de Campo em Poliondas'

p.short_description = (
    "Placa rígida em poliondas para sinalização externa e em campo: "
    "resistente à chuva e ao sol, leve, fácil de fixar. Ideal para PDV "
    "externo, eventos esportivos, obras e ações temporárias — impressão "
    "UV em alta resolução nas 2 faces."
)

p.description = (
    "A Placa de Campo NGD é fabricada em polipropileno corrugado "
    "(poliondas) de 3 mm — o mesmo material premium usado nos nossos "
    "totens e displays. Substitui com vantagem placas de papelão, PVC "
    "fino e madeira fina: resiste à umidade da chuva, não enverga ao "
    "sol, é leve e tem custo muito menor.\n\n"
    "Recebe impressão UV em alta resolução, com cores vivas que não "
    "desbotam com a exposição ao tempo — pensada para uso externo de "
    "média duração. A placa pode ser furada com facilidade para fixação "
    "por parafuso, abraçadeira plástica, fitilho ou amarração de "
    "qualquer tipo, dispensando estruturas complexas.\n\n"
    "Onde usa: sinalização rápida em qualquer contexto que precise de "
    "visibilidade externa — ofertas e promoções na entrada do PDV, "
    "placas laterais em eventos esportivos (campos de futebol, quadras, "
    "corridas, regatas), sinalização temporária em obras, placas para "
    "imobiliária (vende-se / aluga-se), feiras agropecuárias, ações de "
    "campanha e divulgação em campo.\n\n"
    "Tamanhos disponíveis: 30×40, 40×60 e 80×100 cm — escolha conforme "
    "a distância de leitura e o espaço de fixação. A arte pode ser "
    "impressa em uma face (preço menor) ou nas duas (visibilidade "
    "dos dois lados)."
)

p.meta_title = "Placa de Campo em Poliondas Personalizada | NGD"
p.meta_description = (
    "Placa em poliondas 3mm com impressão UV em alta resolução para "
    "sinalização externa: PDV, eventos esportivos, obras, imobiliárias, "
    "feiras. Tamanhos 30×40, 40×60 e 80×100 cm. Envio para todo o Brasil."
)
p.save()
print(f'OK Produto atualizado: {p.name}')
print(f'  short_desc: {len(p.short_description)} chars')
print(f'  description: {len(p.description)} chars')
print(f'  meta_title:  {p.meta_title}')
print()
print('=== Variantes (preservadas) ===')
for v in p.variants.all().order_by('price'):
    print(f'  {v.sku} | {v.size_label} | R$ {v.price}')
