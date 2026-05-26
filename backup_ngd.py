"""Backup automatizado do NGD Site.

Faz:
  1) Dump do Postgres (.sql.gz) usando credenciais do .env
  2) Zip da pasta media/ (uploads do admin — não vão pro git)
  3) Mantém últimos N backups, remove os mais antigos

Como rodar:
  ./venv/Scripts/python backup_ngd.py

Pra rodar diariamente no Windows:
  Task Scheduler → Create Basic Task → Daily 03:00 →
  Action: "C:\\projetos\\NGDSITE\\venv\\Scripts\\python.exe"
  Args:   "C:\\projetos\\NGDSITE\\backup_ngd.py"
  Start in: "C:\\projetos\\NGDSITE"

Em produção (Linux):
  crontab -e
  0 3 * * * cd /caminho/NGDSITE && ./venv/bin/python backup_ngd.py >> logs/backup.log 2>&1
"""
import os
import sys
import shutil
import subprocess
import gzip
from datetime import datetime
from pathlib import Path

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.conf import settings

# === Configuração ===
PROJECT = Path(__file__).resolve().parent
BACKUP_DIR = PROJECT / "backups"
BACKUP_DIR.mkdir(exist_ok=True)
KEEP_LAST = 7   # mantém últimos 7 backups (1 semana)

stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
db_file = BACKUP_DIR / f"ngd-db-{stamp}.sql.gz"
media_file = BACKUP_DIR / f"ngd-media-{stamp}.zip"

print(f"=== Backup NGD Site — {stamp} ===")
print(f"Pasta de destino: {BACKUP_DIR}")
print()


# --- 1) Dump do Postgres ---
db = settings.DATABASES['default']
engine = db.get('ENGINE', '')

if 'postgresql' in engine:
    print("[1/2] Dump do Postgres...")
    env = os.environ.copy()
    env['PGPASSWORD'] = db.get('PASSWORD', '')

    # Tenta achar pg_dump em PATH, ou nos lugares comuns do Windows
    pg_dump = shutil.which('pg_dump')
    if not pg_dump:
        for candidate in [
            r'C:\Program Files\PostgreSQL\18\bin\pg_dump.exe',
            r'C:\Program Files\PostgreSQL\17\bin\pg_dump.exe',
            r'C:\Program Files\PostgreSQL\16\bin\pg_dump.exe',
            r'C:\Program Files\PostgreSQL\15\bin\pg_dump.exe',
            '/usr/bin/pg_dump',
            '/usr/local/bin/pg_dump',
        ]:
            if Path(candidate).exists():
                pg_dump = candidate
                break

    if not pg_dump:
        print("     ERRO: pg_dump não encontrado. Instale o cliente PostgreSQL ou adicione ao PATH.")
        sys.exit(1)

    cmd = [
        pg_dump,
        '-h', db.get('HOST', 'localhost'),
        '-p', str(db.get('PORT') or '5432'),
        '-U', db.get('USER', 'postgres'),
        '-d', db.get('NAME', ''),
        '--no-owner',
        '--no-acl',
    ]
    try:
        with gzip.open(db_file, 'wb') as fout:
            proc = subprocess.run(cmd, env=env, stdout=fout, stderr=subprocess.PIPE, check=True)
        size_mb = db_file.stat().st_size / 1024 / 1024
        print(f"     OK -> {db_file.name} ({size_mb:.1f} MB)")
    except FileNotFoundError:
        print("     ERRO: pg_dump não encontrado no PATH. Instale o cliente PostgreSQL.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"     ERRO: pg_dump falhou. stderr: {e.stderr.decode(errors='ignore')[:500]}")
        sys.exit(1)

elif 'sqlite' in engine:
    print("[1/2] Backup do SQLite (cópia direta)...")
    src = Path(db.get('NAME'))
    dst = BACKUP_DIR / f"ngd-db-{stamp}.sqlite3"
    shutil.copy2(src, dst)
    size_mb = dst.stat().st_size / 1024 / 1024
    print(f"     OK -> {dst.name} ({size_mb:.1f} MB)")
    db_file = dst  # ajusta pro check de rotação

else:
    print(f"ALERTA: engine '{engine}' não tem backup configurado")


# --- 2) Zip da pasta media/ ---
print("[2/2] Compactando pasta media/...")
media_root = Path(settings.MEDIA_ROOT)
if media_root.exists() and any(media_root.iterdir()):
    # shutil.make_archive cria .zip sem extensão
    base = str(media_file).removesuffix('.zip')
    shutil.make_archive(base, 'zip', root_dir=media_root.parent, base_dir=media_root.name)
    size_mb = media_file.stat().st_size / 1024 / 1024
    print(f"     OK -> {media_file.name} ({size_mb:.1f} MB)")
else:
    print(f"     vazio (skip)")
    media_file = None


# --- 3) Rotação (mantém últimos N) ---
print(f"[3/3] Rotação (mantendo últimos {KEEP_LAST} de cada)...")
for prefix in ['ngd-db-', 'ngd-media-']:
    files = sorted(BACKUP_DIR.glob(f"{prefix}*"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in files[KEEP_LAST:]:
        print(f"     removendo: {old.name}")
        old.unlink()

# Tamanho total da pasta de backup
total = sum(f.stat().st_size for f in BACKUP_DIR.iterdir() if f.is_file()) / 1024 / 1024
print()
print(f"=== Concluído. Total de backups armazenados: {total:.1f} MB ===")
