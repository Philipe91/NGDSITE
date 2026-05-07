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
DEBUG = os.getenv("DEBUG", "False") == "True"

SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-dev-only-key-DO-NOT-USE-IN-PRODUCTION"
    else:
        raise RuntimeError(
            "SECRET_KEY ausente. Defina SECRET_KEY no .env antes de rodar com DEBUG=False."
        )

ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

# Origens permitidas para CSRF — túneis de desenvolvimento + valor extra via env (CSRF_TRUSTED_ORIGINS_EXTRA)
CSRF_TRUSTED_ORIGINS = [
    "https://*.loca.lt",
    "https://*.serveo.net",
    "https://*.ngrok-free.app",
    "https://*.pinggy.link",
    "https://*.trycloudflare.com",
]
_extra_trusted = os.getenv("CSRF_TRUSTED_ORIGINS_EXTRA", "").strip()
if _extra_trusted:
    CSRF_TRUSTED_ORIGINS += [o.strip() for o in _extra_trusted.split(",") if o.strip()]

# Cookies — sempre HttpOnly e SameSite=Lax (evita roubo via XSS / CSRF cross-site)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = False  # precisa ser legível p/ JS de fetch protegido
CSRF_COOKIE_SAMESITE = "Lax"

# Limites de upload (defesa contra DoS por payload gigante)
DATA_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024   # 30 MB para form data
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10 MB em memória, resto para disco
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# Tamanho máximo de upload de arte (configurável via env, default 50 MB)
ART_UPLOAD_MAX_BYTES = int(os.getenv("ART_UPLOAD_MAX_BYTES", str(50 * 1024 * 1024)))

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
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"
    SECURE_BROWSER_XSS_FILTER = True

    # Em produção exige ALLOWED_HOSTS configurado explicitamente (não localhost default)
    if ALLOWED_HOSTS == ["localhost", "127.0.0.1"]:
        raise RuntimeError(
            "ALLOWED_HOSTS não configurado para produção. Defina ALLOWED_HOSTS no .env."
        )


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
    "django.contrib.sites",
    "image_uploader_widget",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
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
    # WhiteNoise serve estáticos com cache + compressão (precisa vir logo após SecurityMiddleware)
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

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
        # Persistent connections — reduz latência e custo de conexão sob carga
        "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", "60")),
        "CONN_HEALTH_CHECKS": True,
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
USE_THOUSAND_SEPARATOR = True

# =============================================================================
# ARQUIVOS ESTÁTICOS — servidos por WhiteNoise em produção (compressão + cache)
# =============================================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Storage com hash + compressão (gzip/brotli) para cache eterno em prod
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
            if not DEBUG
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}

# =============================================================================
# ARQUIVOS DE MÍDIA (uploads)
# =============================================================================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =============================================================================
# CACHE — local em dev, Redis em prod se REDIS_URL estiver definido
# =============================================================================
_redis_url = os.getenv("REDIS_URL", "").strip()
if _redis_url:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": _redis_url,
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "ngdsite-default",
        }
    }

# =============================================================================
# LOGGING — sempre console; em prod também grava em arquivo rotativo
# =============================================================================
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "ngdsite.log"),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO" if not DEBUG else "DEBUG",
    },
    "loggers": {
        "django.security": {
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

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
# Secret do webhook configurado no painel do Mercado Pago (obrigatório em produção)
MP_WEBHOOK_SECRET = os.getenv("MP_WEBHOOK_SECRET", "")

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

# =============================================================================
# TELEGRAM 
# =============================================================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# =============================================================================
# ALLAUTH (Login de Clientes)
# =============================================================================
# Modern settings to avoid deprecation warnings
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none" # "none", "optional", "mandatory"
LOGIN_REDIRECT_URL = "/cliente/painel/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_ON_GET = True
