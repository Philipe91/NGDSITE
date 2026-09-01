"""Filtro que monta URL absoluta sem duplicar endereço.

Existe por causa de um detalhe que já quebrou o site em produção: quando os
uploads passaram para o Supabase Storage, `imagem.url` deixou de ser um caminho
relativo (`/media/...`) e virou uma URL completa. Os templates colavam o
endereço do site na frente assim mesmo, e o resultado era:

    https://nucleografico.com.brhttps://xxx.supabase.co/storage/...

Que não abre em lugar nenhum — e ia nas meta tags de compartilhamento e nos
dados estruturados do Google.

Uso no template:

    {% load urls_absolutas %}
    <meta property="og:image" content="{{ produto.featured_image.url|absoluta }}">

Serve para os dois casos: com Storage remoto devolve a URL como está; com
arquivos locais, prefixa o endereço do site.
"""

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def absoluta(url):
    """URL completa, seja o arquivo local ou num Storage remoto."""
    if not url:
        return ""
    texto = str(url)
    # Espaço em URL quebra a prévia de link no WhatsApp e no Facebook, e há
    # arquivo estático com espaço no nome ("LOGO NGD.png").
    texto = texto.replace(" ", "%20")
    if texto.startswith(("http://", "https://", "//")):
        return texto
    if not texto.startswith("/"):
        texto = "/" + texto
    return settings.CANONICAL_BASE + texto
