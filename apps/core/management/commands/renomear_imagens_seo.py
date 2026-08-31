"""Renomeia as imagens dos produtos para nomes que o Google entende.

Uso:
    python manage.py renomear_imagens_seo --simular    # mostra o de/para
    python manage.py renomear_imagens_seo              # renomeia
    python manage.py renomear_imagens_seo --desfazer backups/renomeacao-imagens-....json

Por que existe: hoje os arquivos se chamam coisas como
`Gemini_Generated_Image_ngtxengtxengtxen.png` ou
`ChatGPT_Image_11_de_mai._de_2026_15_21_40.png`. O nome do arquivo é um dos
sinais que o Google usa para entender uma imagem, e esses não dizem nada — além
de anunciarem que a imagem foi gerada por IA, o que não ajuda num site que vende
fábrica própria.

O padrão passa a ser o slug do produto:

    products/featured/totem-eliptico-em-poliondas.png
    products/gallery/totem-eliptico-em-poliondas-02.png
    products/modelos/display-de-chao-modelo-com-prateleiras.png

Segurança: o arquivo é copiado para o nome novo e só então o antigo é apagado,
dentro de uma transação junto com a atualização do banco. Cada execução grava um
mapa de/para em backups/, e `--desfazer` devolve os nomes originais. Funciona
igual no disco local e no Supabase Storage.
"""

import json
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from apps.catalog.models import Product, ProductImage, ProductModelOption

# .jpeg e .JPG viram .jpg — nome curto e consistente
EXTENSOES = {".jpeg": ".jpg", ".jpe": ".jpg"}


def extensao_limpa(nome):
    ext = Path(nome).suffix.lower()
    return EXTENSOES.get(ext, ext)


class Command(BaseCommand):
    help = "Renomeia as imagens dos produtos usando o slug, para leitura do Google."

    def add_arguments(self, parser):
        parser.add_argument(
            "--simular",
            action="store_true",
            help="Mostra o de/para sem renomear nada.",
        )
        parser.add_argument(
            "--desfazer",
            metavar="ARQUIVO",
            help="Devolve os nomes originais a partir de um mapa gravado em backups/.",
        )

    def handle(self, *args, **options):
        if options["desfazer"]:
            return self._desfazer(options["desfazer"])

        simular = options["simular"]
        planejado = self._planejar()

        if not planejado:
            self.stdout.write(self.style.SUCCESS(
                "Todas as imagens já estão com nome adequado. Nada a fazer."
            ))
            return

        self.stdout.write(f"{len(planejado)} imagens para renomear:")
        self.stdout.write("")
        for item in planejado:
            self.stdout.write(f"  {item['de']}")
            self.stdout.write(self.style.SUCCESS(f"  -> {item['para']}"))
            self.stdout.write("")

        if simular:
            self.stdout.write(self.style.WARNING(
                "Simulação: nada foi alterado. Rode sem --simular para aplicar."
            ))
            return

        feitos = self._aplicar(planejado)
        caminho = self._gravar_mapa(feitos)

        self.stdout.write(self.style.SUCCESS(f"{len(feitos)} imagens renomeadas."))
        self.stdout.write(f"Mapa de/para salvo em: {caminho}")
        self.stdout.write(
            "Para voltar atrás:  python manage.py renomear_imagens_seo "
            f"--desfazer {caminho}"
        )

    # ---------------------------------------------------------------- plano
    def _planejar(self):
        """Monta a lista de renomeações, sem tocar em nada ainda."""
        plano = []

        # Ordem estável da galeria, para a numeração não dançar entre execuções
        campos = {f.name for f in ProductImage._meta.fields}
        ordem = ["sort_order", "id"] if "sort_order" in campos else ["id"]

        for produto in Product.objects.all().order_by("id"):
            base = produto.slug

            if produto.featured_image:
                atual = produto.featured_image.name
                novo = f"products/featured/{base}{extensao_limpa(atual)}"
                if atual != novo:
                    plano.append({
                        "modelo": "Product",
                        "pk": produto.pk,
                        "campo": "featured_image",
                        "de": atual,
                        "para": novo,
                    })

            # A capa é a imagem 1, então a galeria começa em 02
            galeria = ProductImage.objects.filter(product=produto).order_by(*ordem)
            for numero, imagem in enumerate(galeria, start=2):
                if not imagem.image:
                    continue
                atual = imagem.image.name
                novo = f"products/gallery/{base}-{numero:02d}{extensao_limpa(atual)}"
                if atual != novo:
                    plano.append({
                        "modelo": "ProductImage",
                        "pk": imagem.pk,
                        "campo": "image",
                        "de": atual,
                        "para": novo,
                    })

            modelos = ProductModelOption.objects.filter(product=produto).order_by("id")
            for opcao in modelos:
                if not opcao.image:
                    continue
                atual = opcao.image.name
                sufixo = slugify(opcao.name) or f"modelo-{opcao.pk}"
                novo = f"products/modelos/{base}-modelo-{sufixo}{extensao_limpa(atual)}"
                if atual != novo:
                    plano.append({
                        "modelo": "ProductModelOption",
                        "pk": opcao.pk,
                        "campo": "image",
                        "de": atual,
                        "para": novo,
                    })

        return plano

    # -------------------------------------------------------------- aplicar
    def _aplicar(self, plano):
        feitos = []
        for item in plano:
            try:
                with transaction.atomic():
                    real = self._mover(item["de"], item["para"])
                    self._gravar_campo(item["modelo"], item["pk"], item["campo"], real)
                feitos.append({**item, "para": real})
            except Exception as erro:
                self.stdout.write(self.style.ERROR(f"  FALHOU {item['de']}: {erro}"))
        return feitos

    def _mover(self, antigo, novo):
        """Copia para o nome novo e só então apaga o antigo."""
        if not default_storage.exists(antigo):
            raise CommandError(f"arquivo não encontrado no storage: {antigo}")

        # Sobra de uma execução interrompida: o nome de destino é único por
        # registro, então o que estiver ali é lixo nosso.
        if default_storage.exists(novo):
            default_storage.delete(novo)

        with default_storage.open(antigo, "rb") as arquivo:
            salvo = default_storage.save(novo, ContentFile(arquivo.read()))

        default_storage.delete(antigo)
        return salvo

    def _gravar_campo(self, nome_modelo, pk, campo, valor):
        modelo = {
            "Product": Product,
            "ProductImage": ProductImage,
            "ProductModelOption": ProductModelOption,
        }[nome_modelo]
        modelo.objects.filter(pk=pk).update(**{campo: valor})

    # ---------------------------------------------------------------- mapa
    def _gravar_mapa(self, feitos):
        pasta = Path(settings.BASE_DIR) / "backups"
        pasta.mkdir(exist_ok=True)
        carimbo = datetime.now().strftime("%Y%m%d-%H%M%S")
        caminho = pasta / f"renomeacao-imagens-{carimbo}.json"
        caminho.write_text(
            json.dumps(feitos, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return caminho.relative_to(Path(settings.BASE_DIR)).as_posix()

    def _desfazer(self, arquivo):
        caminho = Path(arquivo)
        if not caminho.is_absolute():
            caminho = Path(settings.BASE_DIR) / arquivo
        if not caminho.is_file():
            raise CommandError(f"mapa não encontrado: {caminho}")

        feitos = json.loads(caminho.read_text(encoding="utf-8"))
        self.stdout.write(f"Devolvendo {len(feitos)} imagens aos nomes originais...")

        voltaram = 0
        for item in reversed(feitos):
            try:
                with transaction.atomic():
                    real = self._mover(item["para"], item["de"])
                    self._gravar_campo(item["modelo"], item["pk"], item["campo"], real)
                voltaram += 1
            except Exception as erro:
                self.stdout.write(self.style.ERROR(f"  FALHOU {item['para']}: {erro}"))

        self.stdout.write(
            self.style.SUCCESS(f"{voltaram} imagens voltaram ao nome antigo.")
        )
