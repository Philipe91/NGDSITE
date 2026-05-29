"""Remove o travessão (em-dash — e en-dash –) dos textos visíveis,
trocando por vírgula. Mantém × (multiplicação) e · (bullet) intactos.

Aplica em: banco (short_description, description, meta_description de todos
os produtos) + template product_detail.html.
"""
import re
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from pathlib import Path
from apps.catalog.models import Product

EMDASH = '—'  # —
ENDASH = '–'  # –

def fix(text: str) -> str:
    if not text:
        return text
    # " — " ou " – " (com espaços) -> ", "
    text = re.sub(r'\s*[—–]\s*', ', ', text)
    # limpa vírgulas duplicadas geradas (", ," -> ",")
    text = re.sub(r',\s*,', ',', text)
    # limpa ". ," ou "; ,"
    text = re.sub(r'([.;:])\s*,', r'\1', text)
    return text

print("=== BANCO ===")
campos = ['short_description', 'description', 'meta_description', 'meta_title']
for p in Product.objects.all():
    changed = False
    for campo in campos:
        old = getattr(p, campo, '') or ''
        if EMDASH in old or ENDASH in old:
            new = fix(old)
            setattr(p, campo, new)
            changed = True
    if changed:
        p.save()
        print(f'  OK {p.slug}')

print()
print("=== TEMPLATE product_detail.html ===")
tpl = Path('templates/catalog/product_detail.html')
content = tpl.read_text(encoding='utf-8')
before = content.count(EMDASH) + content.count(ENDASH)
content = fix(content)
after = content.count(EMDASH) + content.count(ENDASH)
tpl.write_text(content, encoding='utf-8')
print(f'  travessões: {before} -> {after}')

print()
print("DONE.")
