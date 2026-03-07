import os
import shutil

def copy_slider_images():
    print(" Copiando Imagens para o Static do Front-End...")
    
    # Caminhos
    base_dir = r"E:\NGDSITE"
    source_dir = os.path.join(base_dir, "media", "produtos_mock")
    static_img_dir = os.path.join(base_dir, "static", "img")
    
    # Garante que a pasta static/img existe
    os.makedirs(static_img_dir, exist_ok=True)
    
    # Mapeamento do nome atual para o nome que o HTML do Slider pede
    images_to_copy = {
        "totem_eliptico.png": "totem_ptbr.png",
        "cubo_promocional.png": "cubo_ptbr.png",
        "wobbler_gondola.png": "wobbler_ptbr.png"
    }
    
    sucesso = 0
    for file, new_name in images_to_copy.items():
        src = os.path.join(source_dir, file)
        dst = os.path.join(static_img_dir, new_name)
        
        if os.path.exists(src):
            try:
                shutil.copy2(src, dst)
                print(f" [OK] {new_name} copiada com sucesso.")
                sucesso += 1
            except Exception as e:
                print(f" [ERRO] Falha ao copiar {file}: {e}")
        else:
            print(f" [AVISO] Imagem de origem não encontrada: {src}")
            
    print(f"\nFinalizado! {sucesso} imagens preparadas no static.")

if __name__ == "__main__":
    copy_slider_images()
