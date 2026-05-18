"""Gera variações do Totem Elíptico com tema imobiliário usando Gemini 2.5 Flash Image.
Usa imagem de referência (static/img/ref_totem_eliptico.png) para preservar a forma do produto."""
import os, sys
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERRO: GEMINI_API_KEY não configurada"); sys.exit(1)

client = genai.Client(api_key=API_KEY)

ROOT = Path(__file__).parent
REF = ROOT / "static" / "img" / "ref_totem_eliptico.png"
OUT_DIR = ROOT / "media" / "products" / "featured"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ref_bytes = REF.read_bytes()
ref_part = types.Part.from_bytes(data=ref_bytes, mime_type="image/png")

# 2 prompts diferentes — variando ângulo e cenário, mantendo tema imobiliário
PROMPTS = [
    {
        "name": "totem_eliptico_imob_v1",
        "prompt": (
            "Use the reference image to extract ONLY the physical shape of the elliptical/curved "
            "totem (tall vertical curved display, ~190cm height, freestanding, slightly tapered). "
            "Discard all the existing artwork on it.\n\n"
            "Generate a photorealistic product photo of a SINGLE totem of this elliptical shape, "
            "with completely new artwork applied:\n"
            "- THEME: Brazilian real estate company called 'CASA NOVA'\n"
            "- COLORS: deep navy blue (#0a2553) and white, with gold accents\n"
            "- CONTENT: Top half shows a happy young couple smiling, holding house keys, looking up. "
            "Below, large white text 'CASA NOVA' in modern bold sans-serif. Below that, "
            "promotional text 'SEU IMÓVEL NOVO COMEÇA AQUI' and a sleek modern apartment building "
            "illustration in gold line-art. Bottom shows logo 'CASA NOVA IMÓVEIS'.\n"
            "- STYLE: premium, sophisticated, modern, real estate / banking visual language\n\n"
            "Setting: clean white studio background, soft shadow on floor. The totem is the hero. "
            "Slight 3/4 perspective angle. Sharp focus, professional product photography lighting, "
            "high resolution, hyperrealistic. No people in the scene besides those printed ON the totem."
        ),
    },
    {
        "name": "totem_eliptico_imob_v2",
        "prompt": (
            "Use the reference image to extract ONLY the physical shape of the elliptical/curved "
            "totem (tall vertical curved display, freestanding, slightly tapered). "
            "Discard all existing artwork.\n\n"
            "Generate a photorealistic product photo of TWO totens of this elliptical shape side by side, "
            "with completely new artwork applied:\n"
            "- THEME: Brazilian real estate developer 'VIVA RESIDENCE'\n"
            "- COLORS: light sky blue (#0070f3) and white, with subtle warm beige tones\n"
            "- CONTENT (left totem): photo of a modern luxury apartment building exterior at golden hour, "
            "large bold text 'VIVA RESIDENCE', subtitle 'APARTAMENTOS DE 2 A 4 QUARTOS', and a CTA "
            "'AGENDE SUA VISITA'.\n"
            "- CONTENT (right totem): photo of a happy modern family in a sunny apartment living room, "
            "text 'ENTREGA EM 2026', 'PRONTO PARA MORAR' and a QR code at the bottom.\n"
            "- STYLE: clean, elegant, contemporary real estate marketing, premium feel\n\n"
            "Setting: modern showroom or real estate office, soft natural light through large windows "
            "in the background (slightly blurred). Hardwood floor. Sharp focus on the totens. "
            "Professional product photography, hyperrealistic, high resolution."
        ),
    },
]

print(f"REF: {REF}")
print(f"OUT: {OUT_DIR}\n")

for spec in PROMPTS:
    print(f"[...] Gerando: {spec['name']}...")
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[ref_part, spec["prompt"]],
        )
    except Exception as e:
        print(f"  ERRO: {e}\n")
        continue

    saved = False
    for part in resp.candidates[0].content.parts:
        if getattr(part, "inline_data", None) and part.inline_data.data:
            out = OUT_DIR / f"{spec['name']}.png"
            out.write_bytes(part.inline_data.data)
            print(f"  OK Salvo: {out.relative_to(ROOT)} ({len(part.inline_data.data)/1024:.0f}KB)\n")
            saved = True
            break
        elif getattr(part, "text", None):
            print(f"  Texto retornado: {part.text[:200]}")

    if not saved:
        print(f"  ALERTA: Nenhuma imagem retornada\n")
