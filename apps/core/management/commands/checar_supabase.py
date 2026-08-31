"""Confere se o Supabase está ligado corretamente, ANTES de qualquer deploy.

Uso:
    python manage.py checar_supabase

Três verificações:

  1. Banco       conecta e mostra em qual schema o Django vai criar as tabelas.
  2. Isolamento  tenta ler as tabelas do site oficial. O certo é NÃO CONSEGUIR.
  3. Storage     grava, lê e apaga um arquivo de teste no bucket do catálogo.

Nenhuma delas altera o site que já está no ar: a checagem de isolamento é uma
leitura que deve falhar, e o arquivo de teste do Storage vai para o bucket do
catálogo e é apagado em seguida.
"""

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db import connection, transaction

# Tabelas do site oficial. O usuário do catálogo não pode enxergar nenhuma.
TABELAS_DO_SITE = [
    "blog_posts",
    "services",
    "portfolio_items",
    "hero_slides",
    "clients",
    "contact_submissions",
]

ARQUIVO_DE_TESTE = "_checagem/checar_supabase.txt"


class Command(BaseCommand):
    help = "Confere banco, isolamento e Storage do Supabase antes do deploy."

    def handle(self, *args, **options):
        resultados = [
            self._verificar_banco(),
            self._verificar_isolamento(),
            self._verificar_storage(),
        ]

        self.stdout.write("")
        if all(resultados):
            self.stdout.write(self.style.SUCCESS(
                "Tudo certo. Pode seguir para o deploy."
            ))
        else:
            self.stdout.write(self.style.ERROR(
                "Há pendências acima. Não faça o deploy antes de resolver."
            ))

    # ------------------------------------------------------------------ banco
    def _verificar_banco(self):
        self.stdout.write(self.style.MIGRATE_HEADING("1. Banco de dados"))
        cfg = settings.DATABASES["default"]

        try:
            with connection.cursor() as cur:
                cur.execute("select current_database(), current_user, current_schema()")
                banco, usuario, schema = cur.fetchone()
                cur.execute("show search_path")
                caminho = cur.fetchone()[0]
        except Exception as erro:
            self.stdout.write(self.style.ERROR(f"   Não conectou: {erro}"))
            return False

        self.stdout.write(f"   host     {cfg['HOST']}:{cfg['PORT']}")
        self.stdout.write(f"   banco    {banco}")
        self.stdout.write(f"   usuário  {usuario}")
        self.stdout.write(f"   schema   {schema}   (search_path: {caminho})")

        alertas = []
        local = cfg["HOST"] in ("localhost", "127.0.0.1", "")
        if not local and not cfg.get("OPTIONS", {}).get("sslmode"):
            alertas.append("DB_SSLMODE não está definido — o Supabase exige 'require'.")
        if str(cfg["PORT"]) == "6543" and cfg.get("CONN_MAX_AGE") != 0:
            alertas.append(
                "A porta é a do pooler em modo transação, mas DB_POOLER não está "
                "ligado. Sem isso o site quebra de forma intermitente."
            )
        if settings.DB_SCHEMA and schema != settings.DB_SCHEMA:
            alertas.append(
                f"DB_SCHEMA pede '{settings.DB_SCHEMA}', mas o banco respondeu "
                f"'{schema}'. As tabelas iriam para o lugar errado."
            )

        for alerta in alertas:
            self.stdout.write(self.style.WARNING(f"   ATENÇÃO: {alerta}"))

        if not alertas:
            self.stdout.write(self.style.SUCCESS("   Conexão OK."))
        return not alertas

    # ------------------------------------------------------------- isolamento
    def _verificar_isolamento(self):
        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING(
            "2. Isolamento — o catálogo não pode enxergar as tabelas do site"
        ))

        # Sem banco respondendo, toda consulta falha e o teste passaria por
        # engano — o que seria pior que não testar.
        try:
            with connection.cursor() as cur:
                cur.execute("select 1")
        except Exception:
            self.stdout.write(self.style.ERROR(
                "   Não deu para verificar: o banco não respondeu. "
                "Resolva o item 1 primeiro."
            ))
            return False

        alcancaveis = []
        for tabela in TABELAS_DO_SITE:
            try:
                # Cada tentativa isolada: no Postgres um erro aborta a transação
                with transaction.atomic():
                    with connection.cursor() as cur:
                        cur.execute(f'select 1 from public."{tabela}" limit 1')
                alcancaveis.append(tabela)
            except Exception:
                # Falhar aqui é o comportamento desejado: ou a tabela não existe
                # (projeto separado), ou o usuário não tem permissão (schema
                # isolado). Nos dois casos o site está protegido.
                pass

        if alcancaveis:
            self.stdout.write(self.style.ERROR(
                "   O usuário do catálogo CONSEGUE ler tabelas do site: "
                + ", ".join(alcancaveis)
            ))
            self.stdout.write(self.style.ERROR(
                "   Rode os comandos de REVOKE da seção 3.1 do "
                "deploy/SUBPASTA-LOJA.md antes de continuar."
            ))
            return False

        self.stdout.write(self.style.SUCCESS(
            f"   Nenhuma das {len(TABELAS_DO_SITE)} tabelas do site está ao "
            "alcance. Isolamento confirmado."
        ))
        return True

    # ---------------------------------------------------------------- storage
    def _verificar_storage(self):
        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("3. Storage das imagens"))

        backend = settings.STORAGES["default"]["BACKEND"]
        if "S3Storage" not in backend:
            self.stdout.write(self.style.WARNING(
                "   Storage do Supabase desligado: os uploads vão para media/, "
                "no disco local."
            ))
            self.stdout.write(self.style.WARNING(
                "   Em produção isso faz as fotos sumirem no deploy seguinte. "
                "Preencha as variáveis SUPABASE_S3_* no .env."
            ))
            return False

        self.stdout.write(f"   bucket   {settings.SUPABASE_STORAGE_BUCKET}")

        try:
            nome = default_storage.save(ARQUIVO_DE_TESTE, ContentFile(b"ok"))
            conteudo = default_storage.open(nome).read()
            url = default_storage.url(nome)
            default_storage.delete(nome)
        except Exception as erro:
            self.stdout.write(self.style.ERROR(f"   Falhou: {erro}"))
            return False

        if conteudo != b"ok":
            self.stdout.write(self.style.ERROR(
                "   Gravou mas leu conteúdo diferente do enviado."
            ))
            return False

        self.stdout.write(f"   URL      {url}")
        self.stdout.write(self.style.SUCCESS(
            "   Gravou, leu e apagou o arquivo de teste. Storage OK."
        ))
        return True
