"""Polimento da página da Placa de Campo Poliondas:
foco no posicionamento de INDÚSTRIA DE SINALIZAÇÃO AGRÍCOLA + diferenciais
técnicos (impressão UV direta, corte oscilante, conformidade Lei 10.711)."""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.catalog.models import Product

p = Product.objects.get(slug='placa-de-campo-poliondas')
p.name = 'Placa de Campo em Poliondas'

p.short_description = (
    "Placa em poliondas (3 mm ou 4 mm) para sinalização agrícola, "
    "lavouras e campos de produção de sementes. Fabricada por indústria "
    "(CNAE de Fabricação) com NF e NCM próprios — em conformidade com a "
    "Lei 10.711/2003. Impressão UV direta + corte oscilante de precisão."
)

p.description = (
    "A NGD não é uma gráfica comum: somos uma indústria de sinalização "
    "agrícola. Fabricamos nossas placas seguindo padrões técnicos "
    "rigorosos, com faturamento como indústria (CNAE de Fabricação) e "
    "cada item faturado com seu respectivo código NCM. Atendemos "
    "produtores e sementeiros que precisam estar em conformidade com "
    "a Lei 10.711/2003 (Lei de Sementes) — a placa não é só comunicação "
    "visual, é documento técnico do campo.\n\n"
    "Tecnologia de produção:\n"
    "• Polipropileno corrugado (poliondas) de 3 mm ou 4 mm — espessura "
    "escolhida conforme a exposição e o tempo de campo.\n"
    "• Impressão digital UV direta de alta resolução — cores vivas, "
    "resistentes ao sol e à chuva, sem laminação.\n"
    "• Corte oscilante de alta precisão — encaixes perfeitos, "
    "padronização garantida mesmo em grandes volumes.\n\n"
    "Resultado prático: placa leve, resistente à umidade, fácil de fixar "
    "(parafuso, abraçadeira, fitilho, prego) e com vida útil de campo "
    "muito superior ao papelão ou ao PVC fino — tudo com NF de indústria "
    "para o seu controle fiscal e contábil.\n\n"
    "Usos: sinalização de talhões e quadras em campos de produção de "
    "sementes (Lei 10.711), identificação de variedades e ciclos em "
    "lavouras, demarcação de áreas em fazendas, sinalização em obras "
    "agrícolas, ações de campo, eventos agropecuários e demais "
    "aplicações de sinalização externa.\n\n"
    "Tamanhos padrão: 30×40, 40×60 e 80×100 cm — escolha conforme a "
    "distância de leitura. Impressão em 1 face (4×0) ou 2 faces (4×4). "
    "Para volumes maiores e formatos customizados, fale com a gente."
)

p.meta_title = "Placa de Campo em Poliondas — Sinalização Agrícola (Lei 10.711) | NGD"
p.meta_description = (
    "Indústria de placas em poliondas 3mm e 4mm para sinalização "
    "agrícola, lavouras e campos de sementes — em conformidade com a "
    "Lei 10.711/2003. NF de indústria com NCM. Impressão UV direta + "
    "corte oscilante. Envio para todo o Brasil."
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
