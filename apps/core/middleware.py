"""Middleware customizado de segurança — adiciona headers que o Django
não configura por padrão (CSP, Permissions-Policy)."""
from django.conf import settings
from django.shortcuts import redirect


# Origens permitidas — derivadas do que o site realmente usa hoje (base.html)
CSP_DIRECTIVES = {
    "default-src": ["'self'"],
    "script-src": [
        "'self'",
        "'unsafe-inline'",     # Alpine x-on/x-bind, scripts inline no template
        "'unsafe-eval'",       # Alpine 3.x avalia expressões em runtime
        "https://cdn.jsdelivr.net",         # Alpine.js
        "https://unpkg.com",                # Lucide icons
        "https://connect.facebook.net",     # Meta Pixel
        "https://www.googletagmanager.com", # Google Analytics
        "https://www.google-analytics.com",
    ],
    "style-src": [
        "'self'",
        "'unsafe-inline'",     # Alpine + Tailwind aplicam estilos inline
        "https://fonts.googleapis.com",
    ],
    "font-src": [
        "'self'",
        "https://fonts.gstatic.com",
        "data:",
    ],
    "img-src": [
        "'self'",
        "data:",               # SVGs inline e ícones em data-URI
        "https:",              # imagens de produto/galeria podem vir de CDN externo
    ],
    "connect-src": [
        "'self'",
        "https://www.google-analytics.com",
        "https://www.facebook.com",
        # GA4 direto (23/10/2026): envio dos eventos (region1.google-analytics.com etc.)
        "https://*.google-analytics.com",
        "https://analytics.google.com",     # onde o gtag.js manda o /g/collect hoje
        "https://*.analytics.google.com",
        "https://www.googletagmanager.com",
    ],
    "frame-src": ["'self'"],
    "frame-ancestors": ["'none'"],    # bloqueia ser embed em iframe (anti-clickjacking)
    "base-uri": ["'self'"],
    "form-action": ["'self'"],
    "object-src": ["'none'"],         # bloqueia <object>, <embed> (Flash etc.)
}


def _build_csp_header():
    """Monta a string CSP a partir do dict de diretivas."""
    return "; ".join(
        f"{directive} {' '.join(sources)}"
        for directive, sources in CSP_DIRECTIVES.items()
    )


# Permissions-Policy: desliga APIs do browser que o site não precisa
PERMISSIONS_POLICY = (
    "geolocation=(), "
    "microphone=(), "
    "camera=(), "
    "payment=(), "
    "usb=(), "
    "magnetometer=(), "
    "accelerometer=(), "
    "gyroscope=()"
)


# Prefixos do fluxo de venda — desligados enquanto PORTFOLIO_MODE estiver ligado
ROTAS_DE_VENDA = ("/carrinho/", "/pedidos/", "/pagamento/", "/cliente/", "/accounts/")


class PortfolioModeMiddleware:
    """Tira o fluxo de venda do ar quando PORTFOLIO_MODE está ligado.

    As URLs continuam registradas (para que `{% url %}` e `reverse()` não
    quebrem, e para voltar à loja completa depois é só desligar a flag), mas
    quem acessar essas rotas é mandado de volta para a home.

    A comparação usa `path_info`, e não `path`. Em produção o serviço roda sob
    `FORCE_SCRIPT_NAME=/loja`, e nesse caso `request.path` vem com o prefixo
    ("/loja/carrinho/"), que nunca casa com os prefixos de `ROTAS_DE_VENDA`.
    O `path_info` é o caminho já sem o script name ("/carrinho/"), então é o
    único que funciona tanto local quanto atrás do prefixo.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        caminho = request.path_info
        if (
            settings.PORTFOLIO_MODE
            and caminho.startswith(ROTAS_DE_VENDA)
            and not caminho.startswith("/admin/")
        ):
            return redirect("catalog:home")
        return self.get_response(request)


class SecurityHeadersMiddleware:
    """Adiciona Content-Security-Policy e Permissions-Policy nas respostas.

    CSP é aplicada em todas as páginas EXCETO o admin (que tem comportamento
    JS próprio que pode quebrar com CSP estrito).

    Em DEBUG=True a CSP é enviada como 'Report-Only' — não bloqueia nada, só
    avisaria no console se algo violasse. Útil pra desenvolver sem dor de cabeça.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self._csp_value = _build_csp_header()

    def __call__(self, request):
        response = self.get_response(request)

        # Pula admin (Django admin usa muita coisa que CSP estrito barra)
        if request.path.startswith('/admin/'):
            return response

        # CSP — em DEBUG vai como Report-Only (não bloqueia), em prod enforce
        header_name = (
            "Content-Security-Policy-Report-Only"
            if settings.DEBUG
            else "Content-Security-Policy"
        )
        response.headers[header_name] = self._csp_value

        # Permissions-Policy sempre enforce (apenas desliga APIs não usadas)
        response.headers["Permissions-Policy"] = PERMISSIONS_POLICY

        return response
