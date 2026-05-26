"""Views do app core — utilidades transversais."""
import time
from django.db import connection
from django.http import JsonResponse


def health_check(request):
    """Endpoint público de health check pra UptimeRobot / Cloudflare / monitoramento.

    Responde 200 se o app está vivo E o banco responde rápido.
    Responde 503 se o banco falhou — sinaliza ao monitor pra alertar.

    Retorna JSON com:
      - status: ok | degraded | down
      - db_ms: tempo de query ao banco
      - app: nome da aplicação
    """
    payload = {"status": "ok", "app": "ngdsite"}
    status_http = 200

    # Testa conexão com banco (query trivial)
    t0 = time.perf_counter()
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
        db_ms = round((time.perf_counter() - t0) * 1000, 1)
        payload["db_ms"] = db_ms
        if db_ms > 1000:
            payload["status"] = "degraded"
    except Exception as e:
        payload["status"] = "down"
        payload["db_error"] = str(e)[:200]
        status_http = 503

    return JsonResponse(payload, status=status_http)
