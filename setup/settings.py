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
# MODO PORTFÓLIO
# =============================================================================
# Quando ligado, o site vira vitrine: carrinho, checkout e pagamento saem do ar
# e o CTA passa a ser "Pedir orçamento" via WhatsApp.
# Desligue (PORTFOLIO_MODE=False no .env) para voltar à loja com venda online.
PORTFOLIO_MODE = os.getenv("PORTFOLIO_MODE", "False") == "True"

# Número usado nos links de orçamento (formato internacional, só dígitos)
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "5561996498102")

# Números que dividem o atendimento: o navegador de cada visitante sorteia um
# deles e fica com ele (script no fim do base.html). Separados por vírgula;
# com um só, todo mundo vai para ele.
WHATSAPP_NUMBERS = [
    n.strip() for n in os.getenv("WHATSAPP_NUMBERS", "5561996498102,5561996498279").split(",") if n.strip()
] or [WHATSAPP_NUMBER]

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

    # SITE_URL alimenta canonical, og:url, sitemap e os links de e-mail. Deixá-lo
    # em localhost não quebra nada de forma visível: o site funciona e o Google
    # engole endereços errados por semanas. Por isso falha aqui, e alto.
    if "localhost" in os.getenv("SITE_URL", "http://localhost:8000"):
        raise RuntimeError(
            "SITE_URL não configurado para produção. Defina SITE_URL no .env "
            "com o endereço público (ex.: https://nucleografico.com.br). "
            "É ele que monta canonical, og:url e sitemap."
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
    # Tira carrinho/checkout/pagamento do ar quando PORTFOLIO_MODE=True
    "apps.core.middleware.PortfolioModeMiddleware",
    # CSP + Permissions-Policy (custom — em DEBUG roda como Report-Only)
    "apps.core.middleware.SecurityHeadersMiddleware",
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
                "apps.core.context_processors.site_mode",
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

# Ajustes para banco gerenciado (Supabase). Todos opcionais: sem as variáveis
# no .env, o banco local continua funcionando exatamente como antes.
#
# DB_SCHEMA  — isola as tabelas do catálogo num schema só dele. Use quando o
#              banco for compartilhado com o site oficial, para que as
#              migrations do Django nunca alcancem as tabelas de lá.
# DB_SSLMODE — o Supabase exige conexão criptografada ("require").
# DB_POOLER  — ligue quando o HOST for o pooler em modo transação (porta 6543),
#              que é o indicado para Cloud Run. Nesse modo a conexão não pode
#              ser reaproveitada nem usar cursor no servidor; sem isso o site
#              quebra de forma intermitente e difícil de diagnosticar.
DB_SCHEMA = os.getenv("DB_SCHEMA", "").strip()
DB_SSLMODE = os.getenv("DB_SSLMODE", "").strip()

_db_options = {}
if DB_SSLMODE:
    _db_options["sslmode"] = DB_SSLMODE
if DB_SCHEMA:
    _db_options["options"] = f"-c search_path={DB_SCHEMA},public"
if _db_options:
    DATABASES["default"]["OPTIONS"] = _db_options

if os.getenv("DB_POOLER", "False") == "True":
    DATABASES["default"]["CONN_MAX_AGE"] = 0
    DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True

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

# Uploads no Supabase Storage — mesmo padrão do site oficial.
#
# O nucleografico.com.br guarda tudo que é enviado pelo painel em buckets
# públicos do Supabase (blog, carousel, client-logos, contact-attachments,
# resumes), com as pastas organizadas dentro do bucket e sobrescrita ligada.
# O catálogo segue exatamente esse padrão, só que num bucket próprio, para não
# se misturar com as imagens que já estão no ar.
#
# Enquanto as variáveis abaixo não existirem no .env, nada muda: os uploads
# continuam em MEDIA_ROOT, como hoje.
SUPABASE_S3_ENDPOINT = os.getenv("SUPABASE_S3_ENDPOINT", "").strip().rstrip("/")
SUPABASE_S3_ACCESS_KEY_ID = os.getenv("SUPABASE_S3_ACCESS_KEY_ID", "").strip()
SUPABASE_S3_SECRET_ACCESS_KEY = os.getenv("SUPABASE_S3_SECRET_ACCESS_KEY", "").strip()
# Região real do projeto eisqwuikemthtebpdqbj, verificada em 31/08/2026 pela
# faixa de IP da AWS. Não é sa-east-1: com a região errada o upload falha.
SUPABASE_S3_REGION = os.getenv("SUPABASE_S3_REGION", "us-west-2").strip()
SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "catalogo").strip()

if SUPABASE_S3_ENDPOINT and SUPABASE_S3_ACCESS_KEY_ID and SUPABASE_S3_SECRET_ACCESS_KEY:
    # https://<projeto>.supabase.co/storage/v1/s3 -> https://<projeto>.supabase.co
    _supabase_host = SUPABASE_S3_ENDPOINT.split("/storage/v1")[0]
    # Mesma URL pública que o getPublicUrl() do site gera
    _supabase_publico = f"{_supabase_host}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}"

    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": SUPABASE_STORAGE_BUCKET,
            "endpoint_url": SUPABASE_S3_ENDPOINT,
            "access_key": SUPABASE_S3_ACCESS_KEY_ID,
            "secret_key": SUPABASE_S3_SECRET_ACCESS_KEY,
            "region_name": SUPABASE_S3_REGION,
            # Bucket público: URL limpa, sem assinatura na query
            "querystring_auth": False,
            "custom_domain": _supabase_publico.split("://", 1)[-1],
            # Equivale ao upsert: true usado no painel do site
            "file_overwrite": True,
        },
    }
    MEDIA_URL = _supabase_publico + "/"

# =============================================================================
# MONTAGEM EM SUBCAMINHO (ex.: nucleografico.com.br/loja)
# =============================================================================
# Vazio = servido na raiz, como em dev. Preenchido, o Django passa a gerar
# todo link, redirect e action de formulario ja com o prefixo — {% url %} e
# reverse() respeitam isso sozinhos.
#
# Duas coisas o Django NAO prefixa automaticamente, entao sao feitas aqui:
#   - STATIC_URL
#   - MEDIA_URL, mas so quando as imagens ainda sao locais; com o Supabase
#     ligado ela ja e uma URL absoluta e nao deve ser tocada.
FORCE_SCRIPT_NAME = os.getenv("FORCE_SCRIPT_NAME", "").strip().rstrip("/") or None

if FORCE_SCRIPT_NAME:
    STATIC_URL = f"{FORCE_SCRIPT_NAME}{STATIC_URL}"
    if MEDIA_URL.startswith("/"):
        MEDIA_URL = f"{FORCE_SCRIPT_NAME}{MEDIA_URL}"

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

# Endereço público e definitivo do site, sem barra no fim.
#
# Por que não usar o host da requisição: atrás do Firebase Hosting o Django
# recebe o host interno do Cloud Run (ngd-loja-....run.app), não o domínio que
# o visitante digitou. Montar canonical, og:url e sitemap a partir dele faz o
# Google entender que a loja mora no run.app — jogando fora a autoridade do
# domínio, que é a razão inteira de servir em subpasta.
#
# Daí CANONICAL_BASE sair de uma configuração, não do que chega na porta.
#
# É só o endereço base, SEM caminho: o prefixo da subpasta já vem em
# request.path por causa de FORCE_SCRIPT_NAME. Se SITE_URL vier como
# ".../loja", manter o caminho aqui geraria canonical com /loja/loja/.
from urllib.parse import urlsplit as _urlsplit  # noqa: E402

_endereco = _urlsplit(SITE_URL.strip())
CANONICAL_BASE = (
    f"{_endereco.scheme}://{_endereco.netloc}"
    if _endereco.scheme and _endereco.netloc
    else SITE_URL.rstrip("/")
)

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
# Form de cadastro customizado: PF/PJ + nome/razão + CPF/CNPJ + telefone (p/ NF)
ACCOUNT_SIGNUP_FORM_CLASS = "apps.customers.forms.CustomSignupForm"
LOGIN_REDIRECT_URL = "/cliente/painel/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_ON_GET = True

# Prefixo opcional de URL: permite servir o site inteiro sob uma subpasta do
# dominio oficial (ex.: nucleografico.com.br/loja) sem tocar em template nenhum.
# Basta definir SCRIPT_NAME=/loja no .env; links, canonical, static e media
# passam a sair com o prefixo. Vazio = site na raiz, comportamento de hoje.
SCRIPT_NAME = os.getenv("SCRIPT_NAME", "").strip().rstrip("/")
if SCRIPT_NAME:
    FORCE_SCRIPT_NAME = SCRIPT_NAME
    STATIC_URL = SCRIPT_NAME + STATIC_URL
    # Com o Supabase ligado, MEDIA_URL já é uma URL absoluta e não leva prefixo
    if MEDIA_URL.startswith("/"):
        MEDIA_URL = SCRIPT_NAME + MEDIA_URL
