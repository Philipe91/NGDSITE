"""Copia as imagens de media/ para o bucket do catálogo no Supabase.

Uso:
    python manage.py migrar_media_supabase --simular   # só mostra o que faria
    python manage.py migrar_media_supabase             # envia de verdade

Por que existe: o disco do Cloud Run é descartável. Toda imagem enviada pelo
admin sumiria no deploy seguinte se ficasse dentro do contêiner. Este comando
leva o que já existe em media/ para o Storage, mantendo o mesmo caminho
relativo — products/featured/foto.webp continua products/featured/foto.webp.

Segurança: escreve APENAS no bucket configurado em SUPABASE_STORAGE_BUCKET, que
é o do catálogo. Não encosta nos buckets do site (blog, carousel, client-logos,
contact-attachments, resumes) nem em banco nenhum. Os arquivos locais não são
apagados: media/ continua intacto como cópia de segurança.
"""

from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Envia os arquivos de media/ para o bucket do catálogo no Supabase."

    def add_arguments(self, parser):
        parser.add_argument(
            "--simular",
            action="store_true",
            help="Lista o que seria enviado, sem enviar nada.",
        )
        parser.add_argument(
            "--substituir",
            action="store_true",
            help="Reenvia mesmo os arquivos que já existem no bucket.",
        )
        parser.add_argument(
            "--incluir-uploads",
            action="store_true",
            help=(
                "Envia também media/uploads/, que guarda arquivos enviados por "
                "clientes. Fora por padrão: o bucket é público."
            ),
        )

    def handle(self, *args, **options):
        simular = options["simular"]
        substituir = options["substituir"]

        backend = settings.STORAGES["default"]["BACKEND"]
        if not simular and "S3Storage" not in backend:
            raise CommandError(
                "O Storage do Supabase não está ligado. Preencha as variáveis "
                "SUPABASE_S3_* no .env antes de rodar. Use --simular para "
                "apenas listar os arquivos."
            )

        raiz = Path(settings.MEDIA_ROOT)
        if not raiz.is_dir():
            raise CommandError(f"Pasta não encontrada: {raiz}")

        arquivos = sorted(p for p in raiz.rglob("*") if p.is_file())

        # O bucket do catálogo é público, igual aos do site. Arte enviada por
        # cliente não pode ficar acessível por URL, então media/uploads/ fica
        # de fora a não ser que seja pedido explicitamente.
        if not options["incluir_uploads"]:
            antes = len(arquivos)
            arquivos = [
                p for p in arquivos
                if not p.relative_to(raiz).as_posix().startswith("uploads/")
            ]
            de_cliente = antes - len(arquivos)
            if de_cliente:
                self.stdout.write(self.style.WARNING(
                    f"{de_cliente} arquivos em media/uploads/ ficaram de fora: "
                    "são arquivos de cliente e o bucket é público. "
                    "Use --incluir-uploads se quiser enviá-los mesmo assim."
                ))

        if not arquivos:
            self.stdout.write("Nada em media/ para enviar.")
            return

        total_bytes = sum(p.stat().st_size for p in arquivos)
        destino = "(simulação)" if simular else settings.SUPABASE_STORAGE_BUCKET
        self.stdout.write(
            f"{len(arquivos)} arquivos, {total_bytes / 1048576:.1f} MB "
            f"-> bucket {destino}"
        )
        self.stdout.write("")

        enviados = pulados = falhas = 0

        for caminho in arquivos:
            # products/featured/foto.webp — sempre com barra normal, o Storage
            # não entende a barra invertida do Windows
            relativo = caminho.relative_to(raiz).as_posix()

            if simular:
                self.stdout.write(f"  enviaria  {relativo}")
                enviados += 1
                continue

            try:
                if not substituir and default_storage.exists(relativo):
                    self.stdout.write(f"  já existe {relativo}")
                    pulados += 1
                    continue

                with caminho.open("rb") as arquivo:
                    default_storage.save(relativo, ContentFile(arquivo.read()))

                self.stdout.write(self.style.SUCCESS(f"  enviado   {relativo}"))
                enviados += 1
            except Exception as erro:
                self.stdout.write(self.style.ERROR(f"  FALHOU    {relativo}: {erro}"))
                falhas += 1

        self.stdout.write("")
        resumo = f"{enviados} enviados, {pulados} já existiam, {falhas} falharam"
        if falhas:
            self.stdout.write(self.style.ERROR(resumo))
            self.stdout.write(
                "Rode de novo: o que já subiu é pulado, só as falhas são "
                "tentadas outra vez."
            )
        else:
            self.stdout.write(self.style.SUCCESS(resumo))
            if not simular:
                self.stdout.write(
                    "media/ continua no disco, intacto, como cópia de segurança."
                )
