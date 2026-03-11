import os
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageEnhance
from rembg import remove

def create_tech_design(w, h):
    x, y = np.meshgrid(np.linspace(0, 1, w), np.linspace(0, 1, h))
    R = (0 * x + 0 * y).astype(np.uint8)
    G = (100 * x + 155 * y).astype(np.uint8)
    B = (255 * x + 100 * (1 - y)).astype(np.uint8)
    img = Image.fromarray(np.dstack((R, G, B, np.ones_like(R)*255)), 'RGBA')
    draw = ImageDraw.Draw(img)
    draw.polygon([(0, h), (w, h), (w, h//2), (0, h//3)], fill=(0, 50, 150, 150))
    draw.polygon([(w, 0), (w, h//4), (w//2, 0)], fill=(0, 200, 255, 100))
    return img

def create_energy_design(w, h):
    x, y = np.meshgrid(np.linspace(0, 1, w), np.linspace(0, 1, h))
    R = (20 * x + 10 * y).astype(np.uint8)
    G = (200 * x + 50 * y).astype(np.uint8)
    B = (30 * x + 10 * y).astype(np.uint8)
    img = Image.fromarray(np.dstack((R, G, B, np.ones_like(R)*255)), 'RGBA')
    draw = ImageDraw.Draw(img)
    draw.polygon([(w//4, 0), (w//2, h), (w*3//4, h), (w//2, 0)], fill=(0, 255, 0, 150))
    return img

def create_sale_design(w, h):
    x, y = np.meshgrid(np.linspace(0, 1, w), np.linspace(0, 1, h))
    R = (255 * x + 200 * (1 - x)).astype(np.uint8)
    G = (50 * x + 200 * y).astype(np.uint8)
    B = (0 * x + 0 * y).astype(np.uint8)
    img = Image.fromarray(np.dstack((R, G, B, np.ones_like(R)*255)), 'RGBA')
    draw = ImageDraw.Draw(img)
    c_x, c_y = w//2, h//2
    draw.ellipse((c_x-w//3, c_y-w//3, c_x+w//3, c_y+w//3), fill=(255, 255, 0, 200))
    return img

def create_fresh_design(w, h):
    x, y = np.meshgrid(np.linspace(0, 1, w), np.linspace(0, 1, h))
    R = (50 * x + 150 * y).astype(np.uint8)
    G = (200 * x + 250 * (1 - y)).astype(np.uint8)
    B = (50 * x + 50 * y).astype(np.uint8)
    img = Image.fromarray(np.dstack((R, G, B, np.ones_like(R)*255)), 'RGBA')
    draw = ImageDraw.Draw(img)
    draw.ellipse((w//2, h//2, w*2, h*2), fill=(100, 255, 100, 100))
    return img

def get_font(size):
    try:
        return ImageFont.truetype("arialbd.ttf", size)
    except:
        return ImageFont.load_default()

def process_image(input_path, output_path, theme, title, subtitle):
    orig = Image.open(input_path).convert("RGBA")
    w, h = orig.size
    
    print("Removing background...")
    with open(input_path, 'rb') as f:
        no_bg_bytes = remove(f.read())
    no_bg_img = Image.open(io.BytesIO(no_bg_bytes)).convert("RGBA")
    alpha_mask = no_bg_img.split()[3]
    
    print("Enhancing contrast...")
    enh = ImageEnhance.Contrast(orig)
    orig_contrasted = enh.enhance(1.4).convert("RGB")
    
    print("Generating brand graphics...")
    if theme == 'tech':
        design = create_tech_design(w, h)
    elif theme == 'energy':
        design = create_energy_design(w, h)
    elif theme == 'sale':
        design = create_sale_design(w, h)
    elif theme == 'fresh':
        design = create_fresh_design(w, h)
    else:
        design = create_tech_design(w, h)
    
    draw = ImageDraw.Draw(design)
    font_large = get_font(h // 12)
    font_small = get_font(h // 20)
    
    text_color = (0, 0, 0, 255) if theme == 'sale' else (255, 255, 255, 255)
        
    draw.text((w//2, h//2 - h//15), title, font=font_large, fill=text_color, anchor="mm")
    draw.text((w//2, h//2 + h//15), subtitle, font=font_small, fill=text_color, anchor="mm")
    
    design_rgb = design.convert("RGB")
    
    print("Blending via Multiply...")
    blended_rgb = ImageChops.multiply(orig_contrasted, design_rgb)
    blended_rgba = blended_rgb.convert("RGBA")
    blended_rgba.putalpha(alpha_mask)
    
    print("Compositing on studio background...")
    bg = Image.new("RGBA", orig.size, (245, 245, 245, 255))
    final = Image.alpha_composite(bg, blended_rgba)
    final.save(output_path, "PNG")

base_dir = r"C:\Users\Pc Fechamento\.gemini\antigravity\brain\3c3c17f7-70b3-42a3-ac4d-0994f66701fe"
out_dir = r"c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured"

images = [
    ('totem', os.path.join(base_dir, 'totem_poliondas_1773236276645.png'), 'tech', "TECH CORP", "INOVAÇÃO & DESIGN"),
    ('cubo', os.path.join(base_dir, 'cubo_poliondas_1773236314022.png'), 'energy', "EXTREME", "ENERGY DRINK"),
    ('wobbler', os.path.join(base_dir, 'wobbler_poliondas_1773236338955.png'), 'sale', "MEGA SALE", "-50% OFF"),
    ('faixa', os.path.join(base_dir, 'faixa_poliondas_1773236359461.png'), 'fresh', "MARKET", "PRODUTOS FRESCOS")
]

for name, path, theme, title, subtitle in images:
    if os.path.exists(path):
        out_path = os.path.join(out_dir, f"{name}_branded_mockup.png")
        print(f"\nProcessing {name} with theme {theme}...")
        try:
            process_image(path, out_path, theme, title, subtitle)
            print(f"Saved {out_path}")
        except Exception as e:
            print(f"Error on {name}: {e}")
