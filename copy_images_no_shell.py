import os
import shutil

source_dir = r"C:\Users\Felipe\.gemini\antigravity\brain\e424dd0f-7c7d-4527-8624-0c3cb193e0d9"
target_dir = r"E:\NGDSITE\media\produtos_mock"

os.makedirs(target_dir, exist_ok=True)

images = {
    "totem_eliptico_poliondas_1772925564936.png": "totem_eliptico.png",
    "cubo_promocional_display_1772925579015.png": "cubo_promocional.png",
    "wobbler_gondola_1772925591855.png": "wobbler_gondola.png"
}

for src_name, dest_name in images.items():
    src_path = os.path.join(source_dir, src_name)
    dest_path = os.path.join(target_dir, dest_name)
    # Tenta copiar direto ou falhar silenciosamente pro seed lidar
    try:
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
    except Exception as e:
        pass
