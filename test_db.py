import psycopg
import sys

try:
    conn = psycopg.connect("dbname=postgres user=postgres password=ngd2026 host=127.0.0.1 port=5432")
    cur = conn.cursor()
    cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
    for row in cur.fetchall():
        print(row[0])
except Exception as e:
    print("ERROR:", repr(e))
    sys.exit(1)
