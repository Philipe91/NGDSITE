import os
# Este script Python rodará rapidamente pra criar as pastas do command de seed p/ a gente.
app_cmd_dir = r"E:\NGDSITE\apps\core\management"
app_cmd_sub = r"E:\NGDSITE\apps\core\management\commands"

os.makedirs(app_cmd_sub, exist_ok=True)
with open(os.path.join(app_cmd_dir, "__init__.py"), "w") as f:
    f.write("")
with open(os.path.join(app_cmd_sub, "__init__.py"), "w") as f:
    f.write("")

print("Pastas para commands Django criadas.")
