"""Middleware customizado de segurança — adiciona headers que o Django
não configura por padrão (CSP, Permissions-Policy)."""
from django.conf import settings


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
