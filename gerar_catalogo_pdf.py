# -*- coding: utf-8 -*-
"""
Gera o catálogo NGD em PDF — A4 deitado.

Estrutura: capa, boas-vindas, abertura de produtos, e para cada linha uma
página de abertura (texto + aplicações + foto grande + selos) seguida da
grade de produtos. Fecha com materiais e contracapa.

Como usar:  clique duas vezes em GERAR_CATALOGO_PDF.bat
            (ou: venv\\Scripts\\python.exe gerar_catalogo_pdf.py)

Saída: Catalogo_NGD.pdf, nesta mesma pasta.
Puxa os produtos ATIVOS do banco: cadastrou no admin, rodou de novo,
o catálogo sai atualizado.
"""
import os, sys, io, base64, html, re, subprocess, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
import django
django.setup()

from django.conf import settings
from PIL import Image, ImageFilter
from apps.catalog.models import Product, ProductImage

BASE     = os.path.dirname(os.path.abspath(__file__))
OUT_HTML = os.path.join(BASE, "_catalogo_tmp.html")
# Aceita um caminho de saída alternativo: python gerar_catalogo_pdf.py outro.pdf
OUT_PDF  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "Catalogo_NGD.pdf")

PRIMARY   = "#003366"
SECONDARY = "#00509e"
ACCENT    = "#0070f3"
SURFACE   = "#f7f8fc"
TEXT      = "#1f2937"
MUTED     = "#64748b"

EMAIL = "ngd@nucleografico.com.br"
FONE1 = "(61) 99649-8102"
FONE2 = "(61) 99649-8279"

COLUNAS, LINHAS = 3, 2


# --------------------------------------------------------------- imagens
def img_b64(path, max_px=900, quality=85, keep_alpha=False):
    if not path or not os.path.exists(path):
        return None
    try:
        im = Image.open(path)
    except Exception:
        return None
    im.thumbnail((max_px, max_px), Image.LANCZOS)
    if keep_alpha and im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        fundo = Image.new("RGB", im.size, (255, 255, 255))
        fundo.paste(im, mask=im.split()[-1])
        im = fundo
    else:
        im = im.convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def media(nome):
    return os.path.join(settings.MEDIA_ROOT, nome.replace("/", os.sep)) if nome else None


def static_file(rel):
    for base in [settings.BASE_DIR / "static", settings.BASE_DIR / "staticfiles"]:
        p = os.path.join(str(base), rel.replace("/", os.sep))
        if os.path.exists(p):
            return p
    return None


def galeria(trecho, max_px=1300, quality=84):
    """Busca uma foto da galeria pelo pedaço do nome do arquivo."""
    im = ProductImage.objects.filter(image__icontains=trecho).first()
    return img_b64(media(im.image.name), max_px=max_px, quality=quality) if im else None


def ambiente_b64(trecho):
    """Foto de ambiente já desfocada e reduzida no Pillow.

    Desfocar via CSS faria o Chrome rasterizar a imagem em alta resolução
    e o PDF triplicava de tamanho. Borrando aqui, o arquivo fica leve.
    """
    im = ProductImage.objects.filter(image__icontains=trecho).first()
    caminho = media(im.image.name) if im else None
    if not caminho or not os.path.exists(caminho):
        return None
    try:
        foto = Image.open(caminho).convert("RGB")
    except Exception:
        return None
    foto.thumbnail((620, 620), Image.LANCZOS)
    foto = foto.filter(ImageFilter.GaussianBlur(radius=11))
    buf = io.BytesIO()
    foto.save(buf, "JPEG", quality=68, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def limpa(txt):
    return html.escape((txt or "").strip())


def parse_bullets(desc):
    """Separa a descrição em parágrafos corridos e itens de ficha técnica."""
    desc = (desc or "").replace("**", "").strip()
    paras, bullets = [], []
    for bloco in re.split(r"\n\s*\n", desc):
        for l in [x.strip() for x in bloco.split("\n") if x.strip()]:
            if l.startswith("•"):
                bullets.append(l.lstrip("•").strip())
            elif l.endswith(":") and len(l) < 40:
                continue
            else:
                paras.append(l)
    return paras, bullets


def resumo(p, max_chars=200):
    txt = re.sub(r"\s+", " ", (p.short_description or "").strip())
    if not txt:
        txt = re.sub(r"\s+", " ", (p.description or "").strip())
    if len(txt) <= max_chars:
        return txt
    corte = txt[:max_chars]
    ponto = corte.rfind(". ")
    return corte[:ponto + 1] if ponto > 60 else corte.rstrip() + "..."


LOGO_BRANCA = img_b64(static_file("img/logobranca.png"), max_px=800, keep_alpha=True)
LOGO_AZUL   = img_b64(static_file("img/LOGO NGD.png"), max_px=800, keep_alpha=True)

produtos = list(
    Product.objects.filter(is_active=True)
    .select_related("category")
    .prefetch_related("variants", "images")
)
por_nome = {p.name: p for p in produtos}
n_tamanhos = sum(p.variants.filter(is_active=True).count() for p in produtos)


def grupo(*nomes):
    return [por_nome[n] for n in nomes if n in por_nome]


# --------------------------------------------------------------- seções
SECOES = [
    {
        "titulo": "TOTENS E DISPLAYS",
        "sub": "Setor PDV",
        "texto": "No varejo, quem não é visto não é lembrado. Nossos totens e displays "
                 "transformam corredores comuns em pontos de atenção, com peças leves, "
                 "resistentes e que chegam prontas para uso. Sem suporte, sem ferramenta, "
                 "sem montagem complicada: é posicionar e a peça fica em pé sozinha.",
        "aplicacoes": ["Supermercados e varejo", "Lojas e shoppings",
                       "Halls e recepções", "Eventos e feiras"],
        "ambiente": "Gemini_Generated_Image_hvs01a",
        "produto_foto": "Totem Triangular",
        "selos": [("3mm", "Poliondas", "polipropileno corrugado alveolar"),
                  ("UV", "Impressão UV", "cura a frio, cores vivas, sem odor"),
                  ("360°", "Comunicação total", "faces personalizadas em todos os ângulos"),
                  ("OK", "Pronto para uso", "cortado e vincado, sem montagem")],
        "produtos": grupo("Totem Elíptico", "Totem Triedro em Poliondas", "Totem Triangular",
                          "Totem Réplica em Poliondas", "Display de Chão",
                          "Lixeira Personalizada em Poliondas"),
    },
    {
        "titulo": "EVENTOS E FEIRAS",
        "sub": "Ativação de marca",
        "texto": "Para feira, stand e ação promocional, o que vale é montar rápido, "
                 "transportar fácil e comunicar de longe. São peças modulares que viajam "
                 "planificadas ou dentro de um case, e que se armam em segundos quando "
                 "chegam no destino.",
        "aplicacoes": ["Feiras e stands", "Ações promocionais",
                       "Lançamentos de produto", "Recepções corporativas"],
        "ambiente": "Gemini_Generated_Image_7u4aew",
        "produto_foto": "Cubo Promocional em Poliondas",
        "selos": [("48h", "Produção rápida", "rollup produzido em até 48 horas"),
                  ("380g", "Lona fosca", "sem encanoamento de bordas"),
                  ("KIT", "Case incluso", "base de alumínio e bolsa de transporte"),
                  ("4×0", "Seis faces", "cubo impresso em todas as faces")],
        "produtos": grupo("Banner Rollup", "Cubo Promocional em Poliondas"),
    },
    {
        "titulo": "SINALIZAÇÃO DE CAMPO",
        "sub": "Agro e sementeiros",
        "texto": "Aqui a NGD não atua como gráfica, e sim como indústria de sinalização "
                 "agrícola. Faturamos como fabricação, com CNAE de indústria e NCM próprio "
                 "em cada item. Para o produtor e o sementeiro, a placa deixa de ser "
                 "comunicação visual e passa a ser documento técnico do campo.",
        "aplicacoes": ["Lavouras e talhões", "Campos de produção de sementes",
                       "Identificação de cultivares", "Conformidade Lei 10.711/2003"],
        "ambiente": "placasdecampo01",
        "produto_foto": "Placa de Campo em Poliondas",
        "selos": [("NF", "Nota de indústria", "CNAE de fabricação, NCM por item"),
                  ("LEI", "Lei 10.711/2003", "conformidade para produção de sementes"),
                  ("4mm", "3 mm ou 4 mm", "espessura conforme o tempo de campo"),
                  ("SOL", "Resistente", "não desbota no sol e na chuva")],
        "produtos": grupo("Placa de Campo em Poliondas"),
    },
]

MATERIAIS = [
    ("plastionda.jpg", "Poliondas 3 mm",
     "Polipropileno corrugado alveolar. Leve, resistente à umidade e ao manuseio, "
     "aceita corte, vinco e dobra. É o material dos totens, cubos, lixeiras e placas."),
    ("papelao.jpg", "Papelão microondulado",
     "Alta gramatura, com impressão digital nas faces visíveis. Sai planificado, "
     "o que barateia o frete e facilita o armazenamento. Usado no display de chão."),
    ("papel-duplex.jpg", "Papel Duplex Matte 350 g",
     "Rígido, com acabamento fosco premium e cores fiéis. Corte reto de precisão. "
     "É o material do totem elíptico, para ambientes que pedem mais sofisticação."),
]

paginas = []

# --------------------------------------------------------------- 1. CAPA
paginas.append(f"""
<section class="page capa">
  <div class="capa-marca">
    <img src="{LOGO_AZUL}" alt="NGD">
    <div class="capa-traco"></div>
    <p class="capa-tag">COMUNICAÇÃO VISUAL<br><span>PARA PONTO DE VENDA</span></p>
  </div>
  <div class="capa-pe">
    <span>Catálogo de Produtos</span>
    <span>{FONE1} &nbsp;·&nbsp; {EMAIL}</span>
  </div>
</section>
""")

# --------------------------------------------------------------- 2. BOAS-VINDAS
paginas.append(f"""
<section class="page bem">
  <div class="bem-txt">
    <h2>DO PROJETO<br>À PEÇA PRONTA<br><span>NO SEU PDV</span></h2>
    <p>Somos indústria de comunicação visual. Imprimimos, cortamos, vincamos e
       entregamos a peça pronta para uso, sem terceirizar o meio do caminho.
       Este catálogo reúne nossa linha completa.</p>
    <div class="bem-pill">{EMAIL}</div>
  </div>
  <div class="bem-foto"><img src="{galeria('Gemini_Generated_Image_hvs01a')}" alt=""></div>
</section>
""")

# --------------------------------------------------------------- 3. ABERTURA
paginas.append(f"""
<section class="page statement">
  <div class="st-foto"><img src="{galeria('WhatsApp_Image_2026-02-04')}" alt=""></div>
  <div class="st-veu"></div>
  <div class="st-txt">
    <span class="st-eyebrow">APRESENTAÇÃO DE</span>
    <h1>PRODUTOS</h1>
    <p>Linha completa para ponto de venda, eventos e sinalização de campo.</p>
    <div class="st-nums">
      <div><strong>{len(produtos)}</strong><span>produtos</span></div>
      <div><strong>{n_tamanhos}</strong><span>tamanhos</span></div>
      <div><strong>{len(SECOES)}</strong><span>linhas</span></div>
      <div><strong>UV</strong><span>cura a frio</span></div>
    </div>
  </div>
</section>
""")


# --------------------------------------------------------------- seções
def celula(p):
    foto = img_b64(media(p.featured_image.name), max_px=700, keep_alpha=True) if p.featured_image else None
    tam = [v.size_label for v in p.variants.filter(is_active=True)]
    lista = " &nbsp;·&nbsp; ".join(limpa(t) for t in tam[:3])
    extra = f" +{len(tam) - 3}" if len(tam) > 3 else ""
    return f"""
    <div class="cel">
      <div class="cel-foto">{f'<img src="{foto}">' if foto else ''}</div>
      <div class="cel-txt">
        <h3>{limpa(p.name)}</h3>
        <p>{limpa(resumo(p))}</p>
        <div class="medidas">
          <span class="selo">Tamanhos</span>
          <span class="med-txt">{lista}{extra}</span>
        </div>
      </div>
    </div>"""


def destaque(p):
    """Bloco grande, usado quando a seção tem poucos produtos."""
    foto = img_b64(media(p.featured_image.name), max_px=900, keep_alpha=True) if p.featured_image else None
    tam = [v.size_label for v in p.variants.filter(is_active=True)]
    chips = "".join(f"<span class='chip'>{limpa(t)}</span>" for t in tam)
    thumbs = ""
    for im in p.images.all()[:3]:
        d = img_b64(media(im.image.name), max_px=380, quality=80)
        if d:
            thumbs += f"<div class='mini'><img src='{d}'></div>"
    return f"""
    <div class="dest">
      <div class="dest-foto">{f'<img src="{foto}">' if foto else ''}</div>
      <div class="dest-txt">
        <h3>{limpa(p.name)}</h3>
        <p>{limpa(resumo(p, 320))}</p>
        <span class="rot-min">Tamanhos disponíveis</span>
        <div class="chips">{chips}</div>
        <div class="minis">{thumbs}</div>
      </div>
    </div>"""


def solo(p):
    """Página de um produto só: foto à esquerda, ficha à direita."""
    foto = img_b64(media(p.featured_image.name), max_px=1000, keep_alpha=True) if p.featured_image else None
    tam = [v.size_label for v in p.variants.filter(is_active=True)]
    chips = "".join(f"<span class='chip'>{limpa(t)}</span>" for t in tam)
    thumbs = ""
    for im in p.images.all()[1:4]:
        d = img_b64(media(im.image.name), max_px=420, quality=80)
        if d:
            thumbs += f"<div class='mini'><img src='{d}'></div>"
    paras, _ = parse_bullets(p.description)
    corpo = "".join(f"<p>{limpa(t)}</p>" for t in paras[:2])
    return f"""
    <div class="solo">
      <div class="solo-foto">{f'<img src="{foto}">' if foto else ''}</div>
      <div class="solo-txt">
        <h3>{limpa(p.name)}</h3>
        <p class="solo-lead">{limpa(resumo(p, 260))}</p>
        {corpo}
        <span class="rot-min">Tamanhos disponíveis</span>
        <div class="chips">{chips}</div>
        <div class="minis">{thumbs}</div>
      </div>
    </div>"""


pag = 4
for sec in SECOES:
    selos = "".join(
        f"""<div class="selo-item"><span class="selo-mark">{limpa(m)}</span>
            <div><strong>{limpa(t)}</strong><em>{limpa(d)}</em></div></div>"""
        for m, t, d in sec["selos"]
    )
    aplic = "".join(f"<li>{limpa(a)}</li>" for a in sec["aplicacoes"])
    ambiente = ambiente_b64(sec["ambiente"])
    alvo = por_nome.get(sec["produto_foto"])
    prod_foto = (img_b64(media(alvo.featured_image.name), max_px=1000, keep_alpha=True)
                 if alvo and alvo.featured_image else None)

    paginas.append(f"""
<section class="page abre">
  <div class="abre-txt">
    <h2>{limpa(sec['titulo'])}</h2>
    <span class="abre-sub">{limpa(sec['sub'])}</span>
    <p>{limpa(sec['texto'])}</p>
    <h4>Principais aplicações</h4>
    <ul class="aplic">{aplic}</ul>
  </div>
  <div class="abre-dir">
    <div class="abre-amb">{f'<img src="{ambiente}">' if ambiente else ''}</div>
    <div class="abre-prod">{f'<img src="{prod_foto}">' if prod_foto else ''}</div>
    <div class="selos">{selos}</div>
  </div>
</section>
""")
    pag += 1

    itens = sec["produtos"]
    if len(itens) <= 2:
        blocos = "".join((solo(p) if len(itens) == 1 else destaque(p)) for p in itens)
        paginas.append(f"""
<section class="page">
  <div class="dests">{blocos}</div>
  <footer class="rodape">
    <img class="rod-logo" src="{LOGO_AZUL}" alt="NGD">
    <span class="rod-cta">Peça seu orçamento &nbsp;·&nbsp; WhatsApp {FONE1}</span>
    <span class="rod-pag">{pag:02d}</span>
  </footer>
</section>
""")
        pag += 1
    else:
        passo = COLUNAS * LINHAS
        for i in range(0, len(itens), passo):
            lote = itens[i:i + passo]
            celulas = "".join(celula(p) for p in lote)
            vagas = passo - len(lote)
            if vagas > 0:
                celulas += f"""
    <div class="cel cel-cta" style="grid-column: span {vagas};">
      <h3>Não achou o que precisa?</h3>
      <p>Fabricamos sob medida, no tamanho e no material do seu projeto.</p>
      <span class="cta-fone">WhatsApp {FONE1}</span>
    </div>"""
            paginas.append(f"""
<section class="page">
  <div class="grade">{celulas}</div>
  <footer class="rodape">
    <img class="rod-logo" src="{LOGO_AZUL}" alt="NGD">
    <span class="rod-cta">Peça seu orçamento &nbsp;·&nbsp; WhatsApp {FONE1}</span>
    <span class="rod-pag">{pag:02d}</span>
  </footer>
</section>
""")
            pag += 1

# --------------------------------------------------------------- MATERIAIS
cards = ""
for arq, nome, txt in MATERIAIS:
    d = img_b64(static_file(f"img/materia-prima/{arq}"), max_px=600)
    cards += f"""
    <div class="mat">
      <div class="mat-foto">{f'<img src="{d}">' if d else ''}</div>
      <h3>{limpa(nome)}</h3>
      <p>{limpa(txt)}</p>
    </div>"""

paginas.append(f"""
<section class="page">
  <div class="mat-head">
    <h2>MATERIAIS</h2>
    <span class="abre-sub">O que usamos e por quê</span>
  </div>
  <div class="mats">{cards}</div>
  <footer class="rodape">
    <img class="rod-logo" src="{LOGO_AZUL}" alt="NGD">
    <span class="rod-cta">Peça seu orçamento &nbsp;·&nbsp; WhatsApp {FONE1}</span>
    <span class="rod-pag">{pag:02d}</span>
  </footer>
</section>
""")

# --------------------------------------------------------------- CONTRACAPA
paginas.append(f"""
<section class="page fim">
  <div class="fim-bg"></div>
  <div class="fim-grid">
    <div class="fim-marca"><img src="{LOGO_BRANCA}" alt="NGD"></div>
    <div class="fim-txt"><h2>COMUNICAÇÃO<br>VISUAL<br><span>QUE VENDE</span></h2></div>
  </div>
  <div class="fim-contato">
    <div class="bloco">
      <span class="rot">Contato</span>
      <strong>WhatsApp {FONE1}</strong>
      <strong>Telefone {FONE2}</strong>
      <strong>{EMAIL}</strong>
    </div>
    <div class="bloco">
      <span class="rot">Orçamento</span>
      <p>Envie sua arte ou conte o que precisa.<br>A gente cuida do resto.</p>
    </div>
  </div>
</section>
""")

CSS = f"""
@page {{ size: A4 landscape; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0;
     -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; color: {TEXT}; background: #fff; }}
.page {{ width: 297mm; height: 210mm; position: relative; overflow: hidden;
         page-break-after: always; display: flex; flex-direction: column; background: #fff; }}
.page:last-child {{ page-break-after: auto; }}

/* ---------------- CAPA ---------------- */
.capa {{ align-items: center; justify-content: center;
         background: radial-gradient(circle at 18% 22%, rgba(0,80,158,.07) 0, rgba(0,80,158,0) 42%),
                     radial-gradient(circle at 84% 78%, rgba(0,51,102,.07) 0, rgba(0,51,102,0) 45%), #fff; }}
.capa-marca {{ text-align: center; }}
.capa-marca img {{ width: 92mm; }}
.capa-traco {{ width: 34mm; height: 1.2mm; background: {SECONDARY}; margin: 13mm auto 9mm; border-radius: 2mm; }}
.capa-tag {{ font-size: 13pt; font-weight: 700; letter-spacing: .32em; color: {TEXT}; line-height: 2; }}
.capa-tag span {{ color: {SECONDARY}; }}
.capa-pe {{ position: absolute; left: 0; right: 0; bottom: 14mm; display: flex;
            justify-content: space-between; padding: 0 20mm; font-size: 8.5pt;
            color: {MUTED}; letter-spacing: .06em; }}

/* ---------------- BOAS-VINDAS ---------------- */
.bem {{ flex-direction: row; align-items: center; }}
.bem-txt {{ flex: 1; padding: 0 12mm 0 22mm; }}
.bem-txt h2 {{ font-size: 27pt; font-weight: 800; line-height: 1.14;
               letter-spacing: -0.02em; color: {TEXT}; }}
.bem-txt h2 span {{ color: {SECONDARY}; }}
.bem-txt p {{ margin-top: 8mm; font-size: 10pt; line-height: 1.75; color: {MUTED};
              font-style: italic; max-width: 105mm; }}
.bem-pill {{ margin-top: 10mm; display: inline-block; background: {SURFACE};
             border: .3mm solid #dbe3ee; border-radius: 20mm; padding: 3mm 8mm;
             font-size: 8.5pt; font-weight: 700; letter-spacing: .1em; color: {PRIMARY}; }}
.bem-foto {{ width: 132mm; height: 152mm; margin-right: 20mm; border-radius: 6mm;
             overflow: hidden; flex-shrink: 0; background: {SURFACE}; }}
.bem-foto img {{ width: 100%; height: 100%; object-fit: cover; }}

/* ---------------- STATEMENT ---------------- */
.statement {{ justify-content: center; }}
.st-foto {{ position: absolute; inset: 0; }}
.st-foto img {{ width: 100%; height: 100%; object-fit: cover; }}
.st-veu {{ position: absolute; inset: 0;
           background: linear-gradient(120deg, rgba(0,51,102,.94) 0%, rgba(0,80,158,.88) 55%, rgba(0,112,243,.78) 100%); }}
.st-txt {{ position: relative; z-index: 2; padding: 0 24mm; color: #fff; }}
.st-eyebrow {{ font-size: 11pt; font-weight: 600; letter-spacing: .3em; color: rgba(255,255,255,.7); }}
.st-txt h1 {{ font-size: 62pt; font-weight: 800; letter-spacing: .02em; line-height: 1; margin-top: 3mm; }}
.st-txt > p {{ margin-top: 6mm; font-size: 12pt; color: rgba(255,255,255,.85); }}
.st-nums {{ margin-top: 14mm; display: flex; gap: 16mm; }}
.st-nums div {{ display: flex; flex-direction: column; }}
.st-nums strong {{ font-size: 30pt; font-weight: 800; line-height: 1; }}
.st-nums span {{ margin-top: 2mm; font-size: 8.5pt; text-transform: uppercase;
                 letter-spacing: .18em; color: rgba(255,255,255,.65); }}

/* ---------------- ABERTURA DE SEÇÃO ---------------- */
.abre {{ flex-direction: row; }}
.abre-txt {{ width: 128mm; flex-shrink: 0; padding: 30mm 10mm 0 22mm; }}
.abre-txt h2 {{ font-size: 25pt; font-weight: 800; letter-spacing: -0.02em; color: {TEXT}; line-height: 1.05; }}
.abre-sub {{ display: block; margin-top: 1.5mm; font-size: 17pt; font-weight: 600; color: {SECONDARY}; }}
.abre-txt p {{ margin-top: 9mm; font-size: 9.2pt; line-height: 1.75; color: {MUTED}; font-style: italic; }}
.abre-txt h4 {{ margin-top: 12mm; font-size: 11pt; font-weight: 800; color: {TEXT}; }}
.aplic {{ margin-top: 4mm; list-style: none; }}
.aplic li {{ font-size: 9.5pt; font-weight: 700; font-style: italic;
             color: {SECONDARY}; line-height: 1.85; }}
/* direita = ambiente desfocado ao fundo + produto e selos LADO A LADO */
.abre-dir {{ flex: 1; position: relative; display: flex; align-items: center;
             gap: 6mm; padding: 18mm 12mm 18mm 4mm; overflow: hidden; }}
.abre-amb {{ position: absolute; inset: 0; z-index: 0; }}
.abre-amb img {{ width: 100%; height: 100%; object-fit: cover; opacity: .32; }}
.abre-dir::after {{ content: ''; position: absolute; inset: 0; z-index: 1;
                    background: linear-gradient(90deg, #fff 0%, rgba(255,255,255,.72) 26%, rgba(255,255,255,.5) 100%); }}
.abre-prod {{ position: relative; z-index: 2; flex: 1.3; height: 100%;
              display: flex; align-items: center; justify-content: center; min-width: 0; }}
.abre-prod img {{ max-width: 100%; max-height: 100%; object-fit: contain;
                  border-radius: 4mm; box-shadow: 0 5mm 14mm rgba(15,23,42,.20); }}
.selos {{ position: relative; z-index: 2; flex-shrink: 0;
          display: flex; flex-direction: column; gap: 7mm; }}
.selo-item {{ display: flex; align-items: center; gap: 5mm; }}
.selo-mark {{ width: 17mm; height: 17mm; flex-shrink: 0; border-radius: 3.5mm;
              background: {PRIMARY}; color: #fff; font-size: 9.5pt; font-weight: 800;
              display: flex; align-items: center; justify-content: center;
              box-shadow: 0 2mm 5mm rgba(0,51,102,.25); }}
.selo-item strong {{ display: block; font-size: 11pt; font-weight: 800; color: {TEXT}; }}
.selo-item em {{ display: block; margin-top: .8mm; font-size: 7.6pt;
                 color: {MUTED}; font-style: normal; max-width: 58mm; line-height: 1.4; }}

/* ---------------- GRADE ---------------- */
.grade {{ flex: 1; display: grid; grid-template-columns: repeat({COLUNAS}, 1fr);
          grid-template-rows: repeat({LINHAS}, 1fr); gap: 7mm 9mm;
          padding: 13mm 15mm 6mm; min-height: 0; }}
.cel {{ display: flex; gap: 4.5mm; min-height: 0; align-items: stretch; }}
.cel-foto {{ width: 36mm; height: 100%; flex-shrink: 0; display: flex; align-items: center;
             justify-content: center; background: {SURFACE}; border-radius: 3mm; overflow: hidden; }}
.cel-foto img {{ max-width: 100%; max-height: 100%; object-fit: contain; padding: 2.5mm; }}
.cel-txt {{ flex: 1; display: flex; flex-direction: column; justify-content: center; min-width: 0; }}
.cel-txt h3 {{ font-size: 11.5pt; font-weight: 800; color: {PRIMARY}; line-height: 1.2; }}
.cel-txt p {{ margin-top: 2.5mm; font-size: 7.6pt; line-height: 1.55; color: {MUTED}; }}
.medidas {{ margin-top: 3.5mm; }}
.selo {{ display: inline-block; background: {PRIMARY}; color: #fff; font-size: 5.6pt;
         font-weight: 800; text-transform: uppercase; letter-spacing: .14em;
         padding: 1.3mm 3mm; border-radius: 1mm; }}
.med-txt {{ display: block; margin-top: 1.8mm; font-size: 7.2pt; color: {TEXT}; font-weight: 600; }}
.cel-cta {{ flex-direction: column; justify-content: center; align-items: flex-start;
            background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%);
            border-radius: 3mm; padding: 9mm 11mm; color: #fff; }}
.cel-cta h3 {{ font-size: 15pt; font-weight: 800; }}
.cel-cta p {{ margin-top: 3.5mm; font-size: 8.4pt; line-height: 1.6; color: rgba(255,255,255,.82); }}
.cta-fone {{ margin-top: 6mm; font-size: 11pt; font-weight: 800; }}

/* ---------------- DESTAQUES (seção com poucos produtos) ---------------- */
.dests {{ flex: 1; display: flex; gap: 12mm; padding: 14mm 15mm 6mm; min-height: 0; }}
.dest {{ flex: 1; display: flex; flex-direction: column; min-height: 0; }}
.dest-foto {{ height: 74mm; background: {SURFACE}; border-radius: 4mm; display: flex;
              align-items: center; justify-content: center; overflow: hidden; flex-shrink: 0; }}
.dest-foto img {{ max-width: 100%; max-height: 100%; object-fit: contain; padding: 4mm; }}
.dest-txt h3 {{ margin-top: 6mm; font-size: 16pt; font-weight: 800; color: {PRIMARY}; letter-spacing: -0.01em; }}
.dest-txt p {{ margin-top: 3mm; font-size: 8.6pt; line-height: 1.62; color: {MUTED}; }}
.rot-min {{ display: block; margin-top: 5mm; font-size: 7pt; text-transform: uppercase;
            letter-spacing: .16em; color: {TEXT}; font-weight: 800; }}
.chips {{ margin-top: 2.5mm; display: flex; flex-wrap: wrap; gap: 2mm; }}
.chip {{ background: {SURFACE}; border: .3mm solid #e2e8f0; border-radius: 20mm;
         padding: 1.6mm 3.8mm; font-size: 7.6pt; font-weight: 600; color: #334155; }}
/* produto único ocupando a página */
.solo {{ flex: 1; display: flex; gap: 14mm; min-height: 0; }}
.solo-foto {{ width: 118mm; flex-shrink: 0; background: {SURFACE}; border-radius: 5mm;
              display: flex; align-items: center; justify-content: center; overflow: hidden; }}
.solo-foto img {{ max-width: 100%; max-height: 100%; object-fit: contain; padding: 6mm; }}
.solo-txt {{ flex: 1; display: flex; flex-direction: column; justify-content: center; }}
.solo-txt h3 {{ font-size: 21pt; font-weight: 800; color: {PRIMARY}; letter-spacing: -0.02em; }}
.solo-lead {{ margin-top: 4mm; font-size: 9.6pt; line-height: 1.65; color: {TEXT}; font-weight: 600; }}
.solo-txt > p {{ margin-top: 3.5mm; font-size: 8.4pt; line-height: 1.65; color: {MUTED}; }}

.minis {{ margin-top: 5mm; display: flex; gap: 2.5mm; }}
.mini {{ flex: 1; height: 22mm; background: {SURFACE}; border-radius: 2mm; overflow: hidden; }}
.mini img {{ width: 100%; height: 100%; object-fit: cover; }}

/* ---------------- MATERIAIS ---------------- */
.mat-head {{ padding: 15mm 15mm 0; }}
.mat-head h2 {{ font-size: 25pt; font-weight: 800; letter-spacing: -0.02em; color: {TEXT}; }}
.mats {{ flex: 1; display: flex; align-items: center; gap: 10mm;
         padding: 6mm 15mm; min-height: 0; }}
.mat {{ flex: 1; display: flex; flex-direction: column; }}
.mat-foto {{ height: 66mm; flex-shrink: 0; border-radius: 4mm; overflow: hidden; background: {SURFACE}; }}
.mat-foto img {{ width: 100%; height: 100%; object-fit: cover; }}
.mat h3 {{ margin-top: 6mm; font-size: 13pt; font-weight: 800; color: {PRIMARY}; }}
.mat p {{ margin-top: 3mm; font-size: 8.6pt; line-height: 1.65; color: {MUTED}; }}

/* ---------------- RODAPÉ ---------------- */
.rodape {{ height: 14mm; flex-shrink: 0; display: flex; align-items: center;
           justify-content: space-between; padding: 0 15mm; border-top: .3mm solid #e8eaed; }}
.rod-logo {{ height: 5.5mm; width: auto; }}
.rod-cta {{ font-size: 7.6pt; font-weight: 700; color: {SECONDARY}; letter-spacing: .04em; }}
.rod-pag {{ font-size: 8.5pt; font-weight: 800; color: #c3cddb; }}

/* ---------------- CONTRACAPA ---------------- */
.fim {{ color: #fff; }}
.fim-bg {{ position: absolute; inset: 0;
           background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 70%, {ACCENT} 100%); }}
.fim-bg::after {{ content: ''; position: absolute; right: -60mm; top: -70mm; width: 210mm; height: 210mm;
           border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,.12) 0, rgba(255,255,255,0) 65%); }}
.fim-grid {{ position: relative; z-index: 2; flex: 1; display: flex; align-items: center;
             gap: 18mm; padding: 0 22mm; }}
.fim-marca img {{ width: 78mm; }}
.fim-txt h2 {{ font-size: 30pt; font-weight: 800; line-height: 1.12; letter-spacing: -0.02em; }}
.fim-txt h2 span {{ color: rgba(255,255,255,.55); }}
.fim-contato {{ position: relative; z-index: 2; display: flex; gap: 20mm; padding: 0 22mm 18mm; }}
.bloco {{ display: flex; flex-direction: column; gap: 1.8mm; }}
.rot {{ font-size: 7pt; text-transform: uppercase; letter-spacing: .22em;
        color: rgba(255,255,255,.55); margin-bottom: 1.5mm; }}
.bloco strong {{ font-size: 11pt; font-weight: 700; }}
.bloco p {{ font-size: 9.5pt; line-height: 1.6; color: rgba(255,255,255,.8); }}
"""

doc = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Catálogo NGD</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>{''.join(paginas)}</body></html>"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(doc)

print("Paginas montadas:", len(paginas), "| Produtos:", len(produtos), "| Tamanhos:", n_tamanhos)


# ------------------------------------------------------------------ PDF
def acha_chrome():
    for c in [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]:
        if c and os.path.exists(c):
            return c
    return None


navegador = acha_chrome()
if not navegador:
    print("ERRO: Chrome/Edge nao encontrado. O HTML ficou em:", OUT_HTML)
    sys.exit(1)

perfil = os.path.join(BASE, "_chrome_tmp")
url = "file:///" + OUT_HTML.replace("\\", "/")

if os.path.exists(OUT_PDF):
    try:
        os.remove(OUT_PDF)
    except PermissionError:
        print("ERRO: feche o Catalogo_NGD.pdf antes de gerar de novo.")
        sys.exit(1)

subprocess.run([
    navegador, "--headless=new", "--disable-gpu", "--no-first-run", "--disable-extensions",
    f"--user-data-dir={perfil}", "--virtual-time-budget=30000",
    "--run-all-compositor-stages-before-draw", "--no-pdf-header-footer",
    f"--print-to-pdf={OUT_PDF}", url,
], capture_output=True, timeout=300)

for lixo in (OUT_HTML, perfil):
    try:
        shutil.rmtree(lixo) if os.path.isdir(lixo) else os.remove(lixo)
    except OSError:
        pass

if os.path.exists(OUT_PDF):
    print("PRONTO -> %s (%.1f MB)" % (OUT_PDF, os.path.getsize(OUT_PDF) / 1024 / 1024))
else:
    print("ERRO: o PDF nao foi gerado.")
    sys.exit(1)
