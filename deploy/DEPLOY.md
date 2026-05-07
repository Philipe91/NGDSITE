# Deploy do NGD Site em produção

Resumo rápido para colocar o site no ar com segurança e desempenho profissionais.

## 1. Antes do deploy — checklist obrigatório

- [ ] Gerar `SECRET_KEY` nova (não use a do `.env` de dev):
  ```
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- [ ] Trocar **TODAS** as senhas/tokens que existirem no `.env` de dev (Postgres, Mercado Pago, Telegram, e-mail).
- [ ] Configurar `MP_WEBHOOK_SECRET` no painel do Mercado Pago e copiar para o `.env`.
- [ ] `DEBUG=False` no `.env`.
- [ ] `ALLOWED_HOSTS=seudominio.com.br,www.seudominio.com.br` (sem localhost).
- [ ] `SITE_URL=https://seudominio.com.br`.
- [ ] Rodar `python manage.py check --deploy` e resolver os warnings restantes.
- [ ] Apagar `list_users_temp.py`, `cloudflared.exe` e `backup_*.sql` do servidor.
- [ ] Confirmar que `.env` não está em `git ls-files`.

## 2. Stack de produção recomendada (VPS Ubuntu 22.04)

```
nginx (HTTPS) → Gunicorn (4–8 workers gthread) → Django → PostgreSQL + Redis
```

- **nginx**: termina TLS, serve `/static/` e `/media/`, rate limiting de 1ª camada.
- **Gunicorn**: WSGI com `gthread` para pegar I/O do Mercado Pago/CEP sem bloquear.
- **PostgreSQL**: com `CONN_MAX_AGE=60` no Django para conexões persistentes.
- **Redis** (opcional, recomendado): cache + sessões. Ative com `REDIS_URL=redis://localhost:6379/1`.

## 3. Passo a passo (Ubuntu)

```bash
# 1) Pacotes
sudo apt update
sudo apt install -y python3 python3-venv python3-pip postgresql nginx redis-server

# 2) Criar usuário do app (sem shell, isolado)
sudo adduser --system --group --home /var/www/ngdsite ngdsite

# 3) Clonar repo
sudo -u ngdsite git clone <seu-repo> /var/www/ngdsite
cd /var/www/ngdsite
sudo -u ngdsite python3 -m venv venv
sudo -u ngdsite venv/bin/pip install -r requirements.txt

# 4) .env (copiar de .env.example e preencher)
sudo -u ngdsite cp .env.example .env
sudo -u ngdsite nano .env   # editar valores reais
sudo chmod 600 .env

# 5) Banco de dados
sudo -u postgres createuser ngdsite
sudo -u postgres createdb ngdsite -O ngdsite
sudo -u postgres psql -c "ALTER USER ngdsite WITH PASSWORD 'SENHAFORTE';"

# 6) Migrações + estáticos
sudo -u ngdsite venv/bin/python manage.py migrate
sudo -u ngdsite venv/bin/python manage.py collectstatic --noinput
sudo -u ngdsite venv/bin/python manage.py createsuperuser

# 7) systemd — instala serviço
sudo cp deploy/systemd/ngdsite.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ngdsite
sudo systemctl status ngdsite

# 8) nginx
sudo cp deploy/nginx.conf.example /etc/nginx/sites-available/ngdsite
sudo nano /etc/nginx/sites-available/ngdsite   # ajustar server_name
sudo ln -s /etc/nginx/sites-available/ngdsite /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 9) HTTPS (Let's Encrypt)
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d seudominio.com.br -d www.seudominio.com.br
```

## 4. Deploy em PaaS (Render / Railway / Heroku)

O `Procfile` já está pronto.
1. Conecte o repo.
2. Defina as variáveis de ambiente do `.env.example` no painel do PaaS.
3. Adicione `DEBUG=False` e `ALLOWED_HOSTS=<dominio.do.paas>` (Render põe automático no `.onrender.com`).
4. Crie um **Postgres add-on** e um **Redis add-on**; cole as URLs em `DATABASE_URL`/`REDIS_URL`.
5. O `release` do Procfile já roda `migrate` + `collectstatic`.

## 5. Capacidade — quanto aguenta?

Configuração de referência (VPS 2 vCPU / 4 GB):

| Componente | Config | Tráfego estimado |
|---|---|---|
| Gunicorn | 5 workers × 4 threads | ~100 req/s sustentado |
| nginx limit_req | 30r/s burst 60 | bloqueia floods |
| PostgreSQL CONN_MAX_AGE=60 | reusa conexão | sem gargalo até ~50 req/s |
| Redis cache | sessões + page cache | reduz DB hits 60-80% |
| WhiteNoise | gzip + brotli | estáticos cacheados eternos |

Para escalar mais: mover Postgres para serviço dedicado (RDS/Supabase), CDN (Cloudflare) na frente, multiplicar VPS atrás de um load balancer.

## 6. Monitoramento (recomendado, não bloqueante)

- **Sentry** (`pip install sentry-sdk[django]`) — alerta de erros 500.
- **UptimeRobot** — ping de `/healthz` (criar essa rota se quiser).
- **Postgres `pg_stat_activity`** — ver conexões ativas.
- Logs do Gunicorn vão para `journalctl -u ngdsite -f`.
- Logs Django: `/var/www/ngdsite/logs/ngdsite.log` (rotação automática 5×5MB).

## 7. Checklist após deploy

- [ ] `https://seudominio.com.br` carrega com cadeado.
- [ ] HTTP redireciona pra HTTPS automaticamente.
- [ ] `python manage.py check --deploy` retorna 0 issues.
- [ ] Compra de teste com cartão sandbox MP funciona ponta-a-ponta.
- [ ] Webhook MP marca pedido como pago (logs: `Pedido #X marcado como PAGO`).
- [ ] Upload de arte com PDF de teste funciona; com `.txt` é rejeitado.
- [ ] `/admin/` exige login. Conta admin tem senha forte.
- [ ] Backup diário do Postgres configurado (`pg_dump` em cron).
