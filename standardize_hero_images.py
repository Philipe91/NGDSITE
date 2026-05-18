"""Padroniza imagens do hero slider: todas 1200x1200 RGBA com produto centralizado
ocupando ~90% do canvas. Auto-trim das bordas transparentes/brancas antes."""
from PIL import Image
import numpy as np
from pathlib import Path

TARGET = 1200
FILL_RATIO = 0.92  # ocupação do produto dentro do canvas

IMGS = [
    "static/img/totem_triedro_hero.png",
    "static/img/cubo_ptbr.png",
    "static/img/rollup_hero.png",
    "static/img/totem_eliptico_hero.png",
]

def auto_crop(img: Image.Image) -> Image.Image:
    """Crop bordas transparentes OU quase-brancas."""
    arr = np.array(img)
    if arr.shape[2] == 4:
        # Tem alpha — usa pra detectar conteúdo
        mask = arr[..., 3] > 10
    else:
        # Sem alpha — usa proximidade do branco
        r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
        mask = ~((r >= 240) & (g >= 240) & (b >= 240))
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any():
        return img
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return img.crop((int(cmin), int(rmin), int(cmax) + 1, int(rmax) + 1))

for path_str in IMGS:
    p = Path(path_str)
    if not p.exists():
        print(f"SKIP (não existe): {p}")
        continue

    img = Image.open(p).convert("RGBA")
    original_size = img.size

    # 1. Auto-crop bordas
    img = auto_crop(img)
    cropped = img.size

    # 2. Escalar pra ocupar FILL_RATIO do canvas
    target_inner = int(TARGET * FILL_RATIO)
    scale = min(target_inner / img.width, target_inner / img.height)
    new_w = int(img.width * scale)
    new_h = int(img.height * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # 3. Centralizar em canvas TARGETxTARGET transparente
    canvas = Image.new("RGBA", (TARGET, TARGET), (0, 0, 0, 0))
    x = (TARGET - new_w) // 2
    y = (TARGET - new_h) // 2
    canvas.paste(img, (x, y), img)

    canvas.save(p, optimize=True)
    kb = p.stat().st_size / 1024
    print(f"OK  {p.name:35s} | {original_size[0]:>4}x{original_size[1]:<4} -> trim {cropped[0]:>4}x{cropped[1]:<4} -> canvas {TARGET}x{TARGET} | {kb:>5.0f}KB")

print("\nDONE.")
