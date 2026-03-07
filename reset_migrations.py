import os
import glob

def clear_migrations():
    print(" Limpando o Cache de Migrações do Django...")
    apps_dir = r"E:\NGDSITE\apps"
    
    deleted_count = 0
    # Percorrer todas as apps
    for app in os.listdir(apps_dir):
        app_path = os.path.join(apps_dir, app)
        if os.path.isdir(app_path):
            migrations_dir = os.path.join(app_path, "migrations")
            if os.path.isdir(migrations_dir):
                # Deletar todos os arquivos .py exceto __init__.py 
                for file_path in glob.glob(os.path.join(migrations_dir, "*.py")):
                    if not file_path.endswith("__init__.py"):
                        try:
                            os.remove(file_path)
                            deleted_count += 1
                        except OSError:
                            pass
                            
    print(f"[{deleted_count}] Arquivos de rotas de migração limpos com sucesso.")

if __name__ == "__main__":
    clear_migrations()
