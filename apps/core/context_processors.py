"""
Context processors globais — NGD Site
"""

import os

from django.conf import settings


def _versao_do_css():
    """Data do tailwind.css compilado, usada para furar cache do navegador.

    Sem isso o link fica com uma versao fixa e o navegador continua servindo o
    CSS antigo depois de cada rebuild, o que faz a pagina aparecer quebrada.
    """
    caminho = os.path.join(settings.BASE_DIR, "static", "css", "tailwind.css")
    try:
        # str() porque a localizacao do Django formataria o numero com pontos
        return str(int(os.path.getmtime(caminho)))
    except OSError:
        return "0"


def site_mode(request):
    """Expõe o modo do site e o WhatsApp de orçamento para todos os templates."""
    return {
        "PORTFOLIO_MODE": settings.PORTFOLIO_MODE,
        "WHATSAPP_NUMBER": settings.WHATSAPP_NUMBER,
        "CSS_VERSION": _versao_do_css(),
        # Base de toda URL absoluta (canonical, og:url, dados estruturados).
        # Vem da configuração, nunca do host da requisição: atrás do Firebase
        # o Django enxerga o host interno do Cloud Run. Ver settings.py.
        "CANONICAL_BASE": settings.CANONICAL_BASE,
    }
