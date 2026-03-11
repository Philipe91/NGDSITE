import os
from PIL import Image, ImageOps, ImageEnhance

base_dir = r"C:\Users\Pc Fechamento\.gemini\antigravity\brain\3c3c17f7-70b3-42a3-ac4d-0994f66701fe"

images = {
    'totem': (os.path.join(base_dir, 'totem_poliondas_1773236276645.png'), '#0055ff'),
    'cubo': (os.path.join(base_dir, 'cubo_poliondas_1773236314022.png'), '#00ffaa'),
    'wobbler': (r"c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\wobbler_mock.png", '#ff0055'),
    'faixa': (r"c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\faixa_gondola_1773089535045.png", '#ffaa00')
}

output_dir = r"c:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured"

for key, (img_path, hex_color) in images.items():
    if not os.path.exists(img_path):
        print(f"Skipping {key}, image not found: {img_path}")
        continue
        
    try:
        # Open the image and ensure it has an alpha channel
        img = Image.open(img_path).convert("RGBA")
        
        # Create a solid color image of the same size
        # Convert hex to RGB tuple
        hex_color = hex_color.lstrip('#')
        rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        color_layer = Image.new('RGBA', img.size, rgb_color + (130,))  # 130 is alpha for tint
        
        # Composite the color tint over the original image
        tinted = Image.alpha_composite(img, color_layer)
        
        # To keep the white background white and only tint the product,
        # we can use the original image's brightness/alpha to mask the tint.
        # Simple multiply composite approach:
        # Convert to RGB to apply multiply, then add alpha back if needed
        black_and_white = img.convert("L")
        
        # Colorize takes grayscale and maps black to black, and white to the target color (or vice versa)
        # Here we map white to white and black to the target color for a colorful effect on shadows
        colorized = ImageOps.colorize(black_and_white, black=rgb_color, white="white")
        
        # Enhancing contrast to make it pop
        enhancer = ImageEnhance.Contrast(colorized)
        final_img = enhancer.enhance(1.2)
        
        # Save the result
        out_filename = f"{key}_colored_brand.png"
        out_path = os.path.join(output_dir, out_filename)
        final_img.save(out_path, format="PNG")
        print(f"Generated colored image: {out_filename}")
        
    except Exception as e:
        print(f"Error processing {key}: {e}")

print("Colorization complete.")
