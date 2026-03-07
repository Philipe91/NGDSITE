import os

base_path = r"E:\NGDSITE\apps"
apps = ["core", "catalog", "pages", "orders", "artwork", "customers", "seo"]

if not os.path.exists(base_path):
    os.makedirs(base_path)

for app in apps:
    app_path = os.path.join(base_path, app)
    os.makedirs(app_path, exist_ok=True)
    
    # Criar __init__.py localmente
    init_file = os.path.join(app_path, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('')
    
    # Criar apps.py basem
    apps_file = os.path.join(app_path, "apps.py")
    if not os.path.exists(apps_file):
        with open(apps_file, 'w') as f:
            f.write(f'''from django.apps import AppConfig

class {app.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app}'
''')

print("Pastas Base e Apps Configurados com sucesso.")
