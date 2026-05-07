"""
Configuração do Gunicorn para produção (Linux).

Uso:
    gunicorn -c gunicorn.conf.py setup.wsgi:application
"""
import multiprocessing
import os

# Bind
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")

# Workers — regra clássica: 2 * CPU + 1.
# Use threads quando há I/O (DB/HTTP externo) — caso do checkout/frete/MP.
workers = int(os.getenv("GUNICORN_WORKERS", str(multiprocessing.cpu_count() * 2 + 1)))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gthread")
threads = int(os.getenv("GUNICORN_THREADS", "4"))

# Timeouts — webhook do MP às vezes demora; checkout consulta API de frete.
timeout = int(os.getenv("GUNICORN_TIMEOUT", "60"))
graceful_timeout = 30
keepalive = 5

# Reciclar workers periodicamente para evitar leaks de memória de libs nativas.
max_requests = 1000
max_requests_jitter = 100

# Logs no stdout/stderr — coletados pelo systemd/Docker/PaaS.
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
access_log_format = (
    '%(h)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)ss'
)

# Comportamento
preload_app = True  # carrega Django uma vez antes de fork (economiza RAM)
forwarded_allow_ips = "*"  # confia no proxy reverso (nginx/CDN) p/ X-Forwarded-Proto
