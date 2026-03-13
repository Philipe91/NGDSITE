"""
Django settings for NGD Site — Web-to-Print Platform
Fase 1: Configuração Base
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# =============================================================================
# CAMINHOS BASE
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis do arquivo .env na raiz do projeto
load_dotenv(BASE_DIR / ".env")

# =============================================================================
# SEGURANÇA
# =============================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-insecure-key-apenas-para-dev")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

# Para permitir CSRF (adicionar ao carrinho, finalizar compra) via túneis
CSRF_TRUSTED_ORIGINS = [
    "https://*.loca.lt",
    "https://*.serveo.net",
    "https://*.ngrok-free.app",
    "https://*.pinggy.link"
]

# =============================================================================
# SEGURANÇA EM PRODUÇÃO (ativada quando DEBUG=False)
# =============================================================================
if not DEBUG:
    # Força HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # Cookies seguros (apenas via HTTPS)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS — instrui o navegador a só acessar via HTTPS por 1 ano
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Proteções extras
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_BROWSER_XSS_FILTER = True


# =============================================================================
# APPS INSTALADOS
# =============================================================================
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "apps.core",
    "apps.catalog",
    "apps.pages",
    "apps.orders",
    "apps.customers",
    "apps.seo",
    "apps.cart",
    "apps.payment",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

# =============================================================================
# MIDDLEWARE
# =============================================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =============================================================================
# URLS E WSGI/ASGI
# =============================================================================
ROOT_URLCONF = "setup.urls"
WSGI_APPLICATION = "setup.wsgi.application"

# =============================================================================
# TEMPLATES
# =============================================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.cart.context_processors.cart_processor",
                "apps.catalog.context_processors.totens_processor",
                "apps.seo.context_processors.seo_settings",
            ],
        },
    },
]

# =============================================================================
# BANCO DE DADOS — PostgreSQL
# =============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "ngdsite"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# =============================================================================
# VALIDAÇÃO DE SENHA
# =============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =============================================================================
# INTERNACIONALIZAÇÃO
# =============================================================================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# =============================================================================
# ARQUIVOS ESTÁTICOS
# =============================================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# =============================================================================
# ARQUIVOS DE MÍDIA (uploads)
# =============================================================================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =============================================================================
# CHAVE PADRÃO DE AUTO-CAMPO
# =============================================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============================================================================
# CARRINHO
# =============================================================================
CART_SESSION_ID = "cart"

# =============================================================================
# MERCADO PAGO
# =============================================================================
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN", "")
MP_PUBLIC_KEY = os.getenv("MP_PUBLIC_KEY", "")
MP_SANDBOX = os.getenv("MP_SANDBOX", "True") == "True"

# =============================================================================
# FRETE
# =============================================================================
from decimal import Decimal
SHIPPING_FIXED_COST = Decimal(os.getenv("SHIPPING_FIXED_COST", "25.00"))
STORE_ADDRESS = os.getenv("STORE_ADDRESS", "Av. Principal, 1000 - Centro (confirmar por WhatsApp)")

# =============================================================================
# URL BASE DO SITE (para callbacks do MP)
# =============================================================================
SITE_URL = os.getenv("SITE_URL", "http://localhost:8000")

# =============================================================================
# E-MAIL
# =============================================================================
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "NGD <ngd@nucleografico.com.br>")
