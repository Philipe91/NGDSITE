"""Compressão segura das imagens em media/.
- Resize: max dim 1400px (cobre display retina, web exibe max ~650-800px)
- PNG: optimize=True (sem perder qualidade)
- JPG: quality=85 (visualmente indistinguível, ~75% menor)
- Sobrescreve o arquivo original (user já fez backup)
- Pula imagens já pequenas (< 200KB) e dimensões já razoáveis (< 1500px)
"""
from pathlib import Path
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

MEDIA = Path('media')
MAX_DIM = 1400
SKIP_SIZE_KB = 200
SKIP_DIM = 1500

# Pastas relevantes (uploads do admin)
TARGET_DIRS = ['products/featured', 'products/gallery', 'megamenu', 'categories']

stats = {'processed': 0, 'skipped': 0, 'before': 0, 'after': 0, 'errors': 0}

processed_paths = set()  # dedupe por path absoluto

for sub in TARGET_DIRS:
    base = MEDIA / sub
    if not base.exists():
        continue
    for f in base.rglob('*'):
        if not f.is_file():
            continue
        if f.suffix.lower() not in ('.png', '.jpg', '.jpeg'):
            continue
        # dedupe (Windows é case-insensitive — rglob pode retornar 2x)
        key = str(f.resolve()).lower()
        if key in processed_paths:
            continue
        processed_paths.add(key)

        kb_before = f.stat().st_size / 1024
        try:
            im = Image.open(f)
            w, h = im.size
            big_dim = max(w, h) > SKIP_DIM
            big_file = kb_before > SKIP_SIZE_KB

            if not big_dim and not big_file:
                stats['skipped'] += 1
                continue

            # Preserva alpha em PNG
            if im.mode == 'P':
                im = im.convert('RGBA')

            # Resize proporcional se necessário
            if max(w, h) > MAX_DIM:
                im.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)

            # Salva com base na extensão (mantém formato pra não quebrar refs no DB)
            ext = f.suffix.lower()
            if ext == '.png':
                # Garante RGBA pra preservar transparência
                if im.mode != 'RGBA':
                    im = im.convert('RGBA') if 'transparency' in im.info else im.convert('RGB')
                im.save(f, 'PNG', optimize=True)
            else:  # jpg/jpeg
                # JPG não suporta alpha — converte pra RGB
                if im.mode in ('RGBA', 'LA', 'P'):
                    bg = Image.new('RGB', im.size, (255, 255, 255))
                    bg.paste(im, mask=im.split()[-1] if im.mode == 'RGBA' else None)
                    im = bg
                elif im.mode != 'RGB':
                    im = im.convert('RGB')
                im.save(f, 'JPEG', quality=85, optimize=True, progressive=True)

            kb_after = f.stat().st_size / 1024
            saved_pct = 100 * (1 - kb_after / kb_before) if kb_before else 0
            stats['processed'] += 1
            stats['before'] += kb_before
            stats['after'] += kb_after
            if kb_before > 1000:  # log só as grandes
                print(f'  {kb_before:>6.0f}KB -> {kb_after:>5.0f}KB  ({saved_pct:>4.0f}% menor)  {f.relative_to(MEDIA)}')
        except Exception as e:
            stats['errors'] += 1
            print(f'  ERRO: {f.relative_to(MEDIA)} -> {e}')

print()
print('=' * 60)
print(f'Processadas: {stats["processed"]} imagens')
print(f'Puladas:     {stats["skipped"]} (já pequenas)')
print(f'Erros:       {stats["errors"]}')
print(f'Antes:       {stats["before"]/1024:.0f} MB')
print(f'Depois:      {stats["after"]/1024:.0f} MB')
print(f'Economia:    {(stats["before"]-stats["after"])/1024:.0f} MB ({100*(1-stats["after"]/stats["before"]):.0f}%)')
