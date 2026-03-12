import os
from PIL import Image
import sys

try:
    from rembg import remove
except ImportError:
    print("rembg not installed.")
    sys.exit(1)

input_path = r"C:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\placasdecampo.jpg"
output_path = r"C:\Users\Pc Fechamento\Documents\NGDSITE\static\img\placas_campo_hero.png"

if os.path.exists(input_path):
    print(f"Processing: {input_path}")
    try:
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)
        print(f"Done: saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"File not found: {input_path}")
