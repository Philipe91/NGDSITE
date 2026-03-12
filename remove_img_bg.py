import os
from PIL import Image
import sys

try:
    from rembg import remove
except ImportError:
    print("rembg not fully installed yet. Exiting.")
    sys.exit(1)

image_dir = r"C:\Users\Pc Fechamento\Documents\NGDSITE\static\img"
images_to_process = ["totem_ptbr.png", "cubo_ptbr.png", "wobbler_ptbr.png"]

for img_name in images_to_process:
    input_path = os.path.join(image_dir, img_name)
    
    # We will save the original as a backup just in case
    backup_path = os.path.join(image_dir, img_name.replace(".png", "_backup.png"))
    
    if os.path.exists(input_path):
        if not os.path.exists(backup_path):
            import shutil
            shutil.copyfile(input_path, backup_path)
            
        print(f"Processing: {img_name}...")
        try:
            input_image = Image.open(input_path)
            output_image = remove(input_image)
            output_image.save(input_path)
            print(f"Done: {img_name}")
        except Exception as e:
            print(f"Error processing {img_name}: {e}")
    else:
        print(f"File not found: {img_name}")
