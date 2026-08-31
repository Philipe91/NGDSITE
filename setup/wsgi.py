"""
WSGI config for setup project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

application = get_wsgi_application()


class PrefixoDeSubcaminho:
    """Move o prefixo do caminho de PATH_INFO para SCRIPT_NAME.

    FORCE_SCRIPT_NAME resolve metade do problema: faz o Django *gerar* os links
    com o prefixo. Mas ele nao muda como o Django *interpreta* o caminho que
    chega — a resolucao continua usando PATH_INFO cru. Sem este wrapper, o app
    responde na raiz e devolve 404 em tudo que ele mesmo gerou.

    Importa porque o Firebase Hosting encaminha o caminho **completo** para o
    Cloud Run: um acesso a nucleografico.com.br/loja/x chega aqui como
    PATH_INFO=/loja/x. Aqui o /loja sai do PATH_INFO e vai para o SCRIPT_NAME,
    que e o lugar certo dele.

    Aceita os dois formatos de propósito: com o prefixo (como vem do Firebase)
    e sem (acesso direto a URL do Cloud Run, util para teste).
    """

    def __init__(self, app, prefixo):
        self.app = app
        self.prefixo = (prefixo or '').rstrip('/')

    def __call__(self, environ, start_response):
        caminho = environ.get('PATH_INFO', '')
        if self.prefixo and (caminho == self.prefixo or caminho.startswith(self.prefixo + '/')):
            environ['SCRIPT_NAME'] = self.prefixo
            environ['PATH_INFO'] = caminho[len(self.prefixo):] or '/'
        return self.app(environ, start_response)


_prefixo = os.getenv('FORCE_SCRIPT_NAME', '').strip().rstrip('/')
if _prefixo:
    application = PrefixoDeSubcaminho(application, _prefixo)
