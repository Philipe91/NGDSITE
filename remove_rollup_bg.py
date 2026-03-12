import os
from PIL import Image
import sys
from rembg import remove

input_path = r"C:\Users\Pc Fechamento\Documents\NGDSITE\media\products\featured\banner_rollup_1773089680554.png"
output_path = r"C:\Users\Pc Fechamento\Documents\NGDSITE\static\img\rollup_hero.png"

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
