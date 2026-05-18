"""Re-escala SVGs dos cards de variante (Triedro + Elíptico):
Pessoa silhueta vira referência de 1,80m, totens proporcionalmente menores.

Convenção: 1 cm = 0.68 unidades SVG (pessoa 180cm = 123 unidades; floor em y=145).
"""
import re
from pathlib import Path

p = Path("templates/catalog/product_detail.html")
text = p.read_text(encoding="utf-8")

# ─────────────── Silhueta nova (180cm), cabeça em y=30, pés em y=145 ───────────────
# Pattern A (silhueta centrada em x=98-100, usada em 5 SVGs)
old_silhA = re.compile(
    r'<circle cx="98" cy="52" r="7"/>\s*'
    r'<path d="M88 62 Q98 60 108 62 L110 88 L106 116 L108 144 L102 144 L99 118 L98 100 L97 118 L94 144 L88 144 L90 116 L86 88 Z"/>'
)
new_silhA = (
    '<circle cx="100" cy="30" r="9"/>\n'
    '                                                '
    '<path d="M88 42 Q100 39 112 42 L116 80 L110 130 L112 145 L104 145 L101 132 L100 105 L99 132 L96 145 L88 145 L90 130 L84 80 Z"/>'
)

# Pattern B (silhueta deslocada à direita, em x=105, usada no Triedro 60x190)
old_silhB = re.compile(
    r'<circle cx="105" cy="52" r="7"/>\s*'
    r'<path d="M95 62 Q105 60 115 62 L117 88 L113 116 L115 144 L109 144 L106 118 L105 100 L104 118 L101 144 L95 144 L97 116 L93 88 Z"/>'
)
new_silhB = (
    '<circle cx="107" cy="30" r="9"/>\n'
    '                                                '
    '<path d="M95 42 Q107 39 119 42 L121 80 L115 130 L117 145 L109 145 L107 132 L106 105 L105 132 L102 145 L95 145 L96 130 L91 80 Z"/>'
)

# Pattern C (Elíptico — outro espaço de indentação)
old_silhC = re.compile(
    r'<circle cx="100" cy="52" r="7"/>\s*'
    r'<path d="M90 62 Q100 60 110 62 L112 88 L108 116 L110 144 L104 144 L101 118 L100 100 L99 118 L96 144 L90 144 L92 116 L88 88 Z"/>'
)
new_silhC = (
    '<circle cx="100" cy="30" r="9"/>\n'
    '                                                '
    '<path d="M88 42 Q100 39 112 42 L116 80 L110 130 L112 145 L104 145 L101 132 L100 105 L99 132 L96 145 L88 145 L90 130 L84 80 Z"/>'
)

# Pattern D (Elíptico, silhueta em x=102)
old_silhD = re.compile(
    r'<circle cx="102" cy="52" r="7"/>\s*'
    r'<path d="M92 62 Q102 60 112 62 L114 88 L110 116 L112 144 L106 144 L103 118 L102 100 L101 118 L98 144 L92 144 L94 116 L90 88 Z"/>'
)
new_silhD = (
    '<circle cx="102" cy="30" r="9"/>\n'
    '                                                '
    '<path d="M90 42 Q102 39 114 42 L118 80 L112 130 L114 145 L106 145 L103 132 L102 105 L101 132 L98 145 L90 145 L92 130 L86 80 Z"/>'
)

text = old_silhA.sub(new_silhA, text)
text = old_silhB.sub(new_silhB, text)
text = old_silhC.sub(new_silhC, text)
text = old_silhD.sub(new_silhD, text)

# ─────────────── Re-escalar totens ───────────────
# Fator: 1 cm = 0.683 unidades SVG (123 unidades = 180 cm). Floor em y=145.
# totem_y = 145 - totem_h
REPLACEMENTS = {
    # Triedro
    'totem_h=78 totem_w=22 totem_y=66 face_label="40x120cm"':
        'totem_h=82 totem_w=22 totem_y=63 face_label="40x120cm"',
    'totem_h=120 totem_w=22 totem_y=25 face_label="40x190cm"':
        'totem_h=130 totem_w=22 totem_y=15 face_label="40x190cm"',
    'totem_h=120 totem_w=33 totem_y=25 face_label="60x190cm"':
        'totem_h=130 totem_w=33 totem_y=15 face_label="60x190cm"',
    # Elíptico
    'totem_h=95 totem_w=28 totem_y=50 face_label="50x150cm" top_rx=14':
        'totem_h=103 totem_w=28 totem_y=42 face_label="50x150cm" top_rx=14',
    'totem_h=102 totem_w=34 totem_y=43 face_label="60x160cm" top_rx=17':
        'totem_h=109 totem_w=34 totem_y=36 face_label="60x160cm" top_rx=17',
    'totem_h=115 totem_w=34 totem_y=30 face_label="60x180cm" top_rx=17':
        'totem_h=123 totem_w=34 totem_y=22 face_label="60x180cm" top_rx=17',
}

for old, new in REPLACEMENTS.items():
    if old in text:
        text = text.replace(old, new)
        print(f'OK  {old.split("face_label=")[1].strip()}')
    else:
        print(f'MISS {old.split("face_label=")[1].strip()}')

p.write_text(text, encoding="utf-8")
print("\nDONE.")
