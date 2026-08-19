# -*- coding: utf-8 -*-
"""Cadastra os produtos do catálogo 2026 que ainda não estavam no site.

Idempotente: pode rodar de novo sem duplicar nada. Roda igual nos dois
projetos (venda e portfólio), cada um no seu banco e na sua pasta media/.

Uso:  venv\Scripts\python.exe add_produtos_catalogo_2026.py
"""
import os
import shutil
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

from django.conf import settings
from apps.catalog.models import Category, Product, ProductVariant, ProductImage, ProductModelOption

FOTOS = r"C:\Users\PCFECH~1\AppData\Local\Temp\claude\c--projetos-NGDSITE\cca5d001-76d6-4bcd-a97d-2532d1cf7bdd\scratchpad\ngd\out"


def copia_foto(arquivo, subpasta):
    """Garante a foto em MEDIA_ROOT/<subpasta>/ e devolve o caminho relativo.

    As fotos saem do NGD.pdf (recortadas com o script de extracao). Se a pasta
    de origem nao existir mais, aceita a foto que ja esta em media/.
    """
    destino_dir = os.path.join(settings.MEDIA_ROOT, subpasta)
    destino = os.path.join(destino_dir, arquivo)
    origem = os.path.join(FOTOS, arquivo)
    if os.path.exists(origem):
        os.makedirs(destino_dir, exist_ok=True)
        shutil.copy2(origem, destino)
    elif not os.path.exists(destino):
        raise SystemExit(
            "Foto nao encontrada nem em %s nem em %s. Reextraia do NGD.pdf." % (origem, destino)
        )
    return "%s/%s" % (subpasta, arquivo)


# ---------------------------------------------------------------- mão gigante
def cria_mao_gigante():
    categoria = Category.objects.get(slug="displays-pdv")
    if not categoria.is_active:
        categoria.is_active = True
        categoria.name = "Displays PDV"
        categoria.description = "Peças recortadas e displays de alto impacto para ponto de venda, ativações e eventos."
        categoria.save()

    descricao = (
        "Peça recortada de alto impacto que cria a ilusão de uma mão gigante interagindo com a marca "
        "ou o produto. O formato chama atenção, estimula a interação e funciona especialmente bem em "
        "ativações, lançamentos, eventos, pontos de venda e conteúdos para redes sociais.\n\n"
        "Produzida em poliondas com impressão UV e corte especial no contorno da arte, com base própria "
        "para sustentação. O recorte é desenhado sob medida a partir da sua imagem."
    )

    produto, criado = Product.objects.get_or_create(
        slug="display-recortado-mao-gigante",
        defaults={"category": categoria, "name": "Display de Mão"},
    )
    produto.category = categoria
    produto.name = "Display de Mão"
    produto.short_description = (
        "Display recortado com efeito mão gigante segurando o seu produto. Poliondas com impressão UV e corte especial."
    )
    produto.description = descricao
    produto.meta_title = "Display de Mão, efeito mão gigante | Poliondas com Impressão UV | NGD"
    produto.meta_description = (
        "Display de mão com efeito mão gigante em poliondas, com impressão UV e corte especial no contorno. "
        "Alto impacto para ativações, lançamentos e ponto de venda."
    )
    produto.is_active = True
    produto.is_quote_only = True
    produto.featured_image = copia_foto("mao-gigante-01.jpg", "products/featured")
    produto.save()

    # Galeria: mockups reais da peça (pasta maogigante/ do projeto)
    for ordem, alt in enumerate(GALERIA_MAO, start=1):
        if ordem == 1:
            continue  # foto 01 ja e a capa, repetir deixava duas iguais na galeria
        caminho = copia_foto("mao-gigante-%02d.jpg" % ordem, "products/gallery")
        ProductImage.objects.update_or_create(
            product=produto,
            image=caminho,
            defaults={"alt_text": alt, "sort_order": ordem},
        )

    ProductVariant.objects.update_or_create(
        sku="MAO-GIGANTE-SOB-MEDIDA",
        defaults={
            "product": produto,
            "size_label": "Sob medida",
            "price": 0,
            "weight_kg": 1,
            "length_cm": 5,
            "width_cm": 100,
            "height_cm": 100,
            "is_active": True,
        },
    )
    print("%s produto: %s" % ("criado " if criado else "atualizado", produto.name))


GALERIA_MAO = [
    "Display recortado mão gigante segurando copo personalizado",
    "Display recortado mão gigante segurando embalagem de batata frita",
    "Display recortado mão gigante segurando caneca de chope",
    "Display recortado mão gigante segurando casquinha de sorvete",
    "Display recortado mão gigante segurando prédio de lançamento imobiliário",
    "Display recortado mão gigante segurando placa Seu Novo Lar",
    "Display recortado mão gigante segurando moldura de selfie",
]


# ------------------------------------------------- modelos do display de chão
MODELOS = [
    ("de chão com prateleiras",
     "Estrutura vertical com prateleiras e testeira de destaque para organizar os produtos e ampliar a presença da marca. Entregue planificado para facilitar transporte e armazenamento.",
     "Papelão microondulado · prateleiras e testeira · vai planificado",
     "expositor-prateleiras.png"),
    ("com rodízios",
     "Estrutura móvel que facilita o reposicionamento da campanha dentro do ponto de venda, sem necessidade de desmontagem.",
     "Base com rodízios · sai do estoque montado",
     "expositor-rodizios.png"),
    ("de chão com laterais de comunicação",
     "Quatro níveis de exposição com laterais amplas, transformando praticamente toda a estrutura em espaço para comunicação da marca. A testeira superior reforça a campanha, o produto ou o lançamento.",
     "Quatro níveis · laterais impressas · encaixe com travas",
     "expositor-laterais.png"),
    ("vertical compacto em poliondas",
     "Compacto, leve e funcional, com quatro níveis de exposição, cabeceira ampla e testeiras frontais. Ideal para gerar presença de marca ocupando menos espaço no ponto de venda.",
     "Poliondas 4 mm · quatro níveis · recorte inclinado",
     "expositor-compacto.png"),
    ("de quatro níveis em poliondas",
     "Quatro níveis de exposição combinados a laterais inteiras e saia frontal ampla para comunicação. Estrutura leve, montada por encaixes e pensada para destacar produto e marca em conjunto.",
     "Poliondas 4 mm · quatro níveis · saia frontal ampla",
     "expositor-quatro-niveis.png"),
]


def cria_modelos_display():
    produto = Product.objects.get(slug="display-de-chao")
    for ordem, (nome, descricao, spec, foto) in enumerate(MODELOS, start=1):
        ProductModelOption.objects.update_or_create(
            product=produto,
            name=nome,
            defaults={
                "description": descricao,
                "spec": spec,
                "image": copia_foto(foto, "products/modelos"),
                "sort_order": ordem,
                "is_active": True,
            },
        )
    print("%s modelos no produto: %s" % (len(MODELOS), produto.name))


# ------------------------------------------------ display de chao: modo catálogo
def ajusta_display_chao():
    """Display de Chão vira catálogo: sem formato/preço, orçamento pelo WhatsApp."""
    produto = Product.objects.get(slug="display-de-chao")
    produto.is_quote_only = True
    produto.save()

    # Sem venda online: os tamanhos ficam guardados, mas fora do ar
    produto.variants.update(is_active=False)

    # A galeria fica com as fotos originais do produto: as do catálogo 2026 ficaram
    # repetitivas ao lado da seção "Conheça os modelos", que já mostra as mesmas peças.
    produto.images.filter(image__contains="display-chao-crunchy").delete()
    produto.images.filter(image__startswith="products/modelos/").delete()
    print("display de chao: modo catálogo, %s fotos na galeria" % produto.images.count())


# ------------------------------------------------ eventos: backdrop e pórtico
PRODUTOS_EVENTOS = [
    {
        "slug": "backdrop-para-eventos",
        "nome": "Backdrop para Eventos",
        "foto": "backdrop-eventos.jpg",
        "sku": "BACKDROP-SOB-MEDIDA",
        "curta": ("Painel autoportante de grande formato para palcos, coletivas e pontos de foto. "
                  "Área de marca limpa e contínua, sem precisar furar parede."),
        "longa": ("Painel autoportante de grande formato para palcos, coletivas, eventos e pontos de foto. "
                  "Cria uma área de marca limpa e contínua, com montagem prática e sem necessidade de "
                  "fixação na parede.\n\n"
                  "Estrutura autoportante, impressão contínua e desmontável: sobe rápido, sai rápido e "
                  "volta a ser usado na próxima ação."),
        "meta_titulo": "Backdrop para Eventos | Painel Autoportante Personalizado | NGD",
        "meta_desc": ("Backdrop autoportante de grande formato para palco, coletiva de imprensa e ponto de foto. "
                      "Impressão contínua, montagem sem fixação na parede e estrutura desmontável."),
    },
    {
        "slug": "portico-de-entrada",
        "nome": "Pórtico de Entrada",
        "foto": "portico-entrada.jpg",
        "sku": "PORTICO-SOB-MEDIDA",
        "curta": ("Estrutura de entrada que valoriza a chegada do público e vira ponto de impacto para a "
                  "marca e os patrocinadores."),
        "longa": ("Estrutura de entrada criada para valorizar a chegada do público e gerar um ponto de "
                  "impacto para a marca, patrocinadores e sinalização do evento. Ideal para eventos, "
                  "ativações e áreas externas.\n\n"
                  "Treliça de alumínio com lona tensionada, dimensionada conforme a especificação do projeto."),
        "meta_titulo": "Pórtico de Entrada para Eventos | Treliça e Lona Tensionada | NGD",
        "meta_desc": ("Pórtico de entrada em treliça de alumínio com lona tensionada, para eventos, ativações e "
                      "áreas externas. Projeto sob medida com marca e patrocinadores em destaque."),
    },
]


def cria_produtos_eventos():
    """Backdrop e Pórtico: linha de eventos, sempre sob orçamento."""
    categoria, _ = Category.objects.get_or_create(
        slug="eventos-e-ativacoes",
        defaults={"name": "Eventos e Ativações"},
    )
    categoria.name = "Eventos e Ativações"
    categoria.description = ("Estruturas de grande formato para feira, stand, congresso e ação promocional, "
                             "montadas rápido e reaproveitáveis nas próximas campanhas.")
    categoria.is_active = True
    categoria.save()

    for dados in PRODUTOS_EVENTOS:
        produto, criado = Product.objects.get_or_create(
            slug=dados["slug"], defaults={"category": categoria, "name": dados["nome"]}
        )
        produto.category = categoria
        produto.name = dados["nome"]
        produto.short_description = dados["curta"]
        produto.description = dados["longa"]
        produto.meta_title = dados["meta_titulo"]
        produto.meta_description = dados["meta_desc"]
        produto.is_active = True
        produto.is_quote_only = True
        produto.featured_image = copia_foto(dados["foto"], "products/featured")
        produto.save()

        ProductVariant.objects.update_or_create(
            sku=dados["sku"],
            defaults={
                "product": produto, "size_label": "Sob medida", "price": 0,
                "weight_kg": 1, "length_cm": 10, "width_cm": 100, "height_cm": 100,
                "is_active": True,
            },
        )
        print("%s produto: %s" % ("criado " if criado else "atualizado", produto.name))


if __name__ == "__main__":
    cria_mao_gigante()
    cria_modelos_display()
    ajusta_display_chao()
    cria_produtos_eventos()
