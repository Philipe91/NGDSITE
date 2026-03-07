import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.db import connection

def reset_database():
    print("Iniciando o Reset do Schema Public do Banco de Dados...")
    try:
        with connection.cursor() as cursor:
            # Dropar o schema public inteiro (tabelas, sequencias, etc)
            cursor.execute("DROP SCHEMA public CASCADE;")
            # Recriar o schema limpo
            cursor.execute("CREATE SCHEMA public;")
            # Restaurar permissões padrão (opcional, mas recomendado)
            cursor.execute("GRANT ALL ON SCHEMA public TO postgres;")
            cursor.execute("GRANT ALL ON SCHEMA public TO public;")
            
        print(" Banco Limpo com sucesso!")
        print(" Por favor, execute as migrações em seguida: python manage.py migrate")
    except Exception as e:
        print(f"Erro ao resetar banco de dados: {e}")

if __name__ == "__main__":
    reset_database()
