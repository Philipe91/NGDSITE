import os
import shutil

def copy_slider_images():
    print(" Copiando Imagens Fundo Branco para o Static do Front-End...")
    
    # Caminhos
    static_img_dir = r"E:\NGDSITE\static\img"
    
    # Garante que a pasta static/img existe
    os.makedirs(static_img_dir, exist_ok=True)
    
    # Imagens atuais do cache da IA
    images_to_copy = {
        r"C:\Users\Felipe\.gemini\antigravity\brain\e424dd0f-7c7d-4527-8624-0c3cb193e0d9\totem_ptbr_white_1772926769878.png": "totem_ptbr.png",
        r"C:\Users\Felipe\.gemini\antigravity\brain\e424dd0f-7c7d-4527-8624-0c3cb193e0d9\cubo_ptbr_white_1772926782837.png": "cubo_ptbr.png",
        r"C:\Users\Felipe\.gemini\antigravity\brain\e424dd0f-7c7d-4527-8624-0c3cb193e0d9\wobbler_ptbr_white_1772926796254.png": "wobbler_ptbr.png"
    }
    
    sucesso = 0
    for src, new_name in images_to_copy.items():
        dst = os.path.join(static_img_dir, new_name)
        
        if os.path.exists(src):
            try:
                shutil.copy2(src, dst)
                print(f" [OK] {new_name} atualizada com Fundo Branco.")
                sucesso += 1
            except Exception as e:
                print(f" [ERRO] Falha ao copiar {src}: {e}")
        else:
            print(f" [AVISO] Imagem de origem não encontrada: {src}")
            
    print(f"\nFinalizado! {sucesso} imagens com fundo branco preparadas no static.")

if __name__ == "__main__":
    copy_slider_images()
