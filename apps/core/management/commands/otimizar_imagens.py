"""Converte as imagens do catálogo para WebP, deixando as páginas bem mais leves.

Uso:
    python manage.py otimizar_imagens --simular    # mede o ganho, não grava nada
    python manage.py otimizar_imagens              # converte
    python manage.py otimizar_imagens --desfazer backups/otimizacao-imagens-....json

O problema: as fotos de produto são PNG de até 3 MB em 1400x1400, exibidas em
400px no card. Isso pesa no carregamento, e o tempo de carregamento é um dos
critérios do Google — imagem pesada atrasa justamente o elemento principal da
página, que é o que ele mede.

O que muda: cada imagem vira WebP, redimensionada para no máximo 1200px no maior
lado. Fotografia em WebP costuma ficar entre 5% e 15% do tamanho do PNG, sem
diferença visível.

Reversão: o arquivo original NÃO é apagado. A conversão só troca para onde o
banco aponta, e `--desfazer` devolve o ponteiro. Nada é perdido.

Funciona igual no disco local e no Supabase Storage.
"""

import io
import json
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from PIL import Image, ImageFile

from apps.catalog.models import (
    Category,
    MegaMenuTotensCard,
    Product,
    ProductImage,
    ProductModelOption,
)

ImageFile.LOAD_TRUNCATED_IMAGES = True

LADO_MAXIMO = 1200
QUALIDADE = 82


class Command(BaseCommand):
    help = "Converte as imagens do catálogo para WebP e reduz o peso das páginas."

    def add_arguments(self, parser):
        parser.add_argument(
            "--simular",
            action="store_true",
            help="Mede o ganho sem gravar nada.",
        )
        parser.add_argument(
            "--desfazer",
            metavar="ARQUIVO",
            help="Devolve o banco às imagens originais, a partir de um mapa em backups/.",
        )

    def handle(self, *args, **options):
        if options["desfazer"]:
            return self._desfazer(options["desfazer"])

        simular = options["simular"]
        alvos = self._listar()

        if not alvos:
            self.stdout.write(self.style.SUCCESS(
                "Todas as imagens já estão em WebP. Nada a fazer."
            ))
            return

        self.stdout.write(f"{len(alvos)} imagens para converter.")
        self.stdout.write("")

        antes = depois = 0
        feitos = []

        for item in alvos:
            try:
                bruto = self._ler(item["de"])
                convertido, tamanho_final, dimensoes = self._converter(bruto)
            except Exception as erro:
                self.stdout.write(self.style.ERROR(f"  FALHOU {item['de']}: {erro}"))
                continue

            antes += len(bruto)
            depois += tamanho_final
            corte = 100 - (tamanho_final * 100 // max(len(bruto), 1))

            self.stdout.write(
                "  %-44s %6.0f KB -> %5.0f KB  (-%d%%)  %s"
                % (Path(item["de"]).name[:44], len(bruto) / 1024,
                   tamanho_final / 1024, corte, dimensoes)
            )

            if simular:
                continue

            try:
                with transaction.atomic():
                    # O WebP pode já existir no Storage — é o caso de rodar de
                    # novo apontando para outro banco (produção usa o mesmo
                    # bucket). Reaproveita em vez de criar um arquivo duplicado
                    # com sufixo aleatório.
                    if default_storage.exists(item["para"]):
                        salvo = item["para"]
                    else:
                        salvo = default_storage.save(item["para"], ContentFile(convertido))
                    self._gravar_campo(item["modelo"], item["pk"], item["campo"], salvo)
                feitos.append({**item, "para": salvo})
            except Exception as erro:
                self.stdout.write(self.style.ERROR(
                    f"  FALHOU ao gravar {item['para']}: {erro}"
                ))

        self.stdout.write("")
        self.stdout.write(
            "Total: %.1f MB -> %.1f MB  (%.0f%% mais leve)"
            % (antes / 1048576, depois / 1048576,
               100 - (depois * 100 / max(antes, 1)))
        )

        if simular:
            self.stdout.write(self.style.WARNING(
                "Simulação: nada foi gravado. Rode sem --simular para aplicar."
            ))
            return

        caminho = self._gravar_mapa(feitos)
        self.stdout.write(self.style.SUCCESS(f"{len(feitos)} imagens convertidas."))
        self.stdout.write(f"Mapa salvo em: {caminho}")
        self.stdout.write(
            "Os arquivos originais continuam no storage. Para voltar atrás:\n"
            f"  python manage.py otimizar_imagens --desfazer {caminho}"
        )

    # --------------------------------------------------------------- listagem
    def _listar(self):
        """Imagens que ainda não são WebP, com o nome de destino já definido."""
        alvos = []
        # Todo campo de imagem que aparece nas páginas entra aqui.
        #
        # Fica de fora de propósito:
        # - SEOSettings.og_image_default, e qualquer imagem usada em og:image.
        #   WhatsApp e LinkedIn têm suporte irregular a WebP na prévia de link;
        #   converter troca uma prévia que funciona por uma que pode não abrir.
        # - template_file, manual_file e art_file, que são PDF e arquivo de arte
        #   do cliente, não imagem de página.
        fontes = (
            (Product, "featured_image"),
            (ProductImage, "image"),
            (ProductModelOption, "image"),
            (Category, "image"),
            (MegaMenuTotensCard, "image"),
        )
        for modelo, campo in fontes:
            for obj in modelo.objects.all().order_by("id"):
                arquivo = getattr(obj, campo)
                if not arquivo:
                    continue
                nome = arquivo.name
                if nome.lower().endswith(".webp"):
                    continue
                alvos.append({
                    "modelo": modelo.__name__,
                    "pk": obj.pk,
                    "campo": campo,
                    "de": nome,
                    "para": str(Path(nome).with_suffix(".webp")).replace("\\", "/"),
                })
        return alvos

    # -------------------------------------------------------------- conversão
    def _ler(self, nome):
        if not default_storage.exists(nome):
            raise CommandError("arquivo não encontrado no storage")
        with default_storage.open(nome, "rb") as arquivo:
            return arquivo.read()

    def _converter(self, bruto):
        im = Image.open(io.BytesIO(bruto))

        # PNG com transparência sobre fundo branco: o catálogo é sobre fundo
        # claro, e achatar aqui evita halo escuro nas bordas.
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            fundo = Image.new("RGB", im.size, (255, 255, 255))
            fundo.paste(im, mask=im.split()[-1])
            im = fundo
        else:
            im = im.convert("RGB")

        if max(im.size) > LADO_MAXIMO:
            im.thumbnail((LADO_MAXIMO, LADO_MAXIMO), Image.LANCZOS)

        saida = io.BytesIO()
        im.save(saida, format="WEBP", quality=QUALIDADE, method=6)
        dados = saida.getvalue()
        return dados, len(dados), "%dx%d" % im.size

    def _gravar_campo(self, nome_modelo, pk, campo, valor):
        modelo = {
            "Product": Product,
            "ProductImage": ProductImage,
            "ProductModelOption": ProductModelOption,
            "Category": Category,
            "MegaMenuTotensCard": MegaMenuTotensCard,
        }[nome_modelo]
        modelo.objects.filter(pk=pk).update(**{campo: valor})

    # ------------------------------------------------------------------ mapa
    def _gravar_mapa(self, feitos):
        pasta = Path(settings.BASE_DIR) / "backups"
        pasta.mkdir(exist_ok=True)
        carimbo = datetime.now().strftime("%Y%m%d-%H%M%S")
        caminho = pasta / f"otimizacao-imagens-{carimbo}.json"
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
        voltaram = 0
        for item in feitos:
            if not default_storage.exists(item["de"]):
                self.stdout.write(self.style.ERROR(
                    f"  original sumiu do storage: {item['de']}"
                ))
                continue
            self._gravar_campo(item["modelo"], item["pk"], item["campo"], item["de"])
            voltaram += 1

        self.stdout.write(self.style.SUCCESS(
            f"{voltaram} imagens voltaram ao arquivo original."
        ))
