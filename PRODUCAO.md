# 🚀 NGD SITE — Checklist de Produção e Segurança

> Documento mestre para acompanhar o que falta até o lançamento.
> Marque com `[x]` os itens conforme forem concluídos.
> Última atualização: 2026-05-04

---

## 📊 Status geral

| Área | Status |
|---|---|
| Camada de código (validações, anti-fraude, anti-DoS) | ✅ Blindado |
| Configuração de produção (settings, gunicorn, nginx) | ✅ Pronta — falta plugar |
| Credenciais reais (rotação) | ❌ Pendente |
| Deploy real | ❌ Pendente |
| Monitoramento (Sentry / uptime) | ❌ Pendente |
| Testes automatizados | ❌ Pendente |

---

## 🔥 BLOQUEADORES — não subir em prod sem isto

São coisas que **só você pode fazer** (envolvem contas externas / decisões).

- [ ] **Gerar nova `SECRET_KEY` para produção**
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
  Cole o resultado no `.env` de produção (não no `.env` de dev).

- [ ] **Rotacionar `MP_ACCESS_TOKEN` no Mercado Pago**
  https://www.mercadopago.com.br/developers/panel/app
  → Suas credenciais → Renovar token → atualizar `.env` de prod.

- [ ] **Configurar `MP_WEBHOOK_SECRET`**
  Painel MP → Webhooks → Configurar → copiar a chave secreta para o `.env`.
  Sem isso, em produção o webhook **rejeita** todas as notificações.

- [ ] **Trocar senha do Postgres** (`DB_PASSWORD`)
  A senha `ngd2026` no `.env` de dev é fraca e conhecida. Usar uma senha forte (`openssl rand -base64 24`).

- [ ] **Trocar app password do Gmail** (`EMAIL_HOST_PASSWORD`)
  https://myaccount.google.com/apppasswords → revogar a antiga, gerar uma nova.

- [ ] **Trocar `TELEGRAM_BOT_TOKEN`** (com @BotFather → `/revoke` → `/token`)

- [ ] **Definir `ALLOWED_HOSTS` real** no `.env` de prod (ex: `nucleografico.com.br,www.nucleografico.com.br`)

- [ ] **Definir `SITE_URL`** com domínio real e HTTPS (`https://nucleografico.com.br`)

- [ ] **Decidir hospedagem**: VPS (DigitalOcean / Hetzner / Hostinger) ou PaaS (Render / Railway). Ver [deploy/DEPLOY.md](deploy/DEPLOY.md).

---

## 🧹 Limpeza pré-lançamento

Coisas que existem hoje em desenvolvimento e **não podem** ir pra produção.

### Arquivos a remover do disco do servidor de produção

- [ ] `list_users_temp.py` — script de teste que lista usuários (já no `.gitignore`, mas garantir que não vá no deploy)
- [ ] `cloudflared.exe` — binário local de túnel (já no `.gitignore`)
- [ ] `backup_ngd222.sql` — dump de banco com dados de teste (ainda **rastreado** pelo Git!)
- [ ] `APRESENTACAO_TUNEL.bat` — script de apresentação local
- [ ] Todos os `apply_v*.py`, `update_*.py`, `fix_template*.py` — scripts one-shot do desenvolvimento
- [ ] `triedo.png`, `debug.txt` — arquivos soltos
- [ ] Pasta `media/` em prod deve ser separada da de dev (se for o caso)

### Limpeza no Git

- [ ] **Destrackear o backup SQL**:
  ```bash
  git rm --cached backup_ngd222.sql
  git commit -m "chore: untrack DB backup"
  ```
- [ ] **Apagar do histórico** (opcional, destrutivo — força push):
  ```bash
  pip install git-filter-repo
  git filter-repo --path backup_ngd222.sql --invert-paths
  git push --force origin main   # AVISAR equipe antes
  ```

### Dados fake do banco

- [ ] Listar e remover **pedidos de teste** antes de virar prod
- [ ] Listar e remover **usuários de teste** (especialmente staff/superusers de dev)
- [ ] Conferir se categorias/produtos/preços estão corretos para vendas reais
- [ ] Testar uma compra real ponta-a-ponta com o cartão de teste do Mercado Pago em **sandbox**, depois em produção com valor mínimo (R$ 1,00 por exemplo)

---

## 🔒 SEGURANÇA — o que já está pronto

> Não precisa marcar — está implementado e funciona automaticamente quando `DEBUG=False`.

- [x] Webhook Mercado Pago com **HMAC-SHA256** (apps/payment/views.py)
- [x] Webhook **confere valor pago vs `Order.total`** (anti-fraude)
- [x] Webhook é **idempotente** (mesmo payment_id não atualiza duas vezes)
- [x] Checkout **recalcula preço** do banco — ignora valor da sessão (anti-tampering)
- [x] Checkout **recalcula frete** do servidor — ignora valor enviado pelo cliente
- [x] Quantidade no carrinho **clampada `[1, 999]`** (sem negativos / overflow)
- [x] Checkout em **`@transaction.atomic`** (sem pedidos órfãos)
- [x] Variantes inativas **bloqueadas** no checkout
- [x] Upload de arte: **extensão + content-type + magic bytes + tamanho + sanitização do nome**
- [x] Sessão de convidado só vale após **pedido criado** (flag `customer_email_verified`)
- [x] Rate limiting: checkout 30/min, upload 20/min, frete 60/min, webhook 120/min, todos por IP
- [x] Cookies `HttpOnly` e `SameSite=Lax` por padrão; `Secure` em prod
- [x] HSTS (1 ano), CSP de frame `DENY`, `nosniff`, `Referrer-Policy: same-origin` em prod
- [x] HTTPS forçado em prod (`SECURE_SSL_REDIRECT`)
- [x] `SECRET_KEY` ausente em prod **dispara erro** no boot
- [x] `ALLOWED_HOSTS=localhost` em prod **dispara erro** no boot
- [x] Limites de upload globais: 30 MB form, 10 MB memory, 1000 fields max

---

## 🔒 SEGURANÇA — itens recomendados (ordem de prioridade)

- [ ] **`django-axes`** — bloqueia conta após N tentativas de senha (anti-brute-force)
  ```bash
  pip install django-axes
  ```
  Adicionar a `INSTALLED_APPS`, `MIDDLEWARE` e `AUTHENTICATION_BACKENDS` (ver docs).

- [ ] **2FA para admin** — `django-otp` + `django-two-factor-auth`
  Crítico se vai dar acesso a mais alguém na equipe ao admin.

- [ ] **Endpoint de health check** `/healthz` que retorne 200 se DB ok
  Necessário pra UptimeRobot / load balancer.

- [ ] **Política de senha mais forte** — adicionar validador customizado em `AUTH_PASSWORD_VALIDATORS` (ex: exigir 1 número + 1 maiúscula + 12+ caracteres)

- [ ] **Auditar uso de `|safe` nos templates**
  Atualmente em uso:
  - `templates/pages/page_detail.html` — conteúdo HTML do CMS (admin trusted, ok se admin não for comprometido)
  - `templates/admin/dashboard.html` — chart_labels/chart_data (vem de `json.dumps`, ok)

- [ ] **CSP (Content-Security-Policy)** — `pip install django-csp`
  Boa prática: define quais scripts/imagens podem carregar. Reduz superfície de XSS mesmo se algo escapar.

- [ ] **Backups automáticos do Postgres** (cron de `pg_dump` + envio para S3/B2)

- [ ] **Auditoria de acesso ao admin** — `LogEntry` já registra; criar dashboard ou exportar pra log externo.

- [ ] **Verificar OAuth do Google** se for ativar (allauth está pronto, mas há um fix de DoesNotExist no commit `f059191`)

---

## 🚦 PERFORMANCE & ESCALA — o que já está pronto

- [x] **WhiteNoise** com manifest + gzip/brotli pra estáticos (cache eterno em prod)
- [x] **Postgres `CONN_MAX_AGE=60`** (conexões persistentes)
- [x] Configuração de **Redis cache** habilitada via `REDIS_URL` (opcional)
- [x] **Logging rotativo** em `logs/ngdsite.log` (5 arquivos × 5 MB)
- [x] **Gunicorn** configurado com `gthread`, preload, max_requests rotativo
- [x] **nginx** de exemplo com gzip, rate limit, cache de estáticos

---

## 🚦 PERFORMANCE & ESCALA — itens a fazer

- [ ] **Provisionar Redis** em produção (DigitalOcean Managed Redis / Render Redis / Railway Redis)
  → Setar `REDIS_URL` no `.env` de prod
  → Sessões e cache de templates já vão usar automaticamente

- [ ] **Cache de fragmentos de template** nas páginas de catálogo:
  ```django
  {% load cache %}
  {% cache 600 catalog_home %}
    ... markup pesado ...
  {% endcache %}
  ```
  Reduz hits no banco em 60-80% pra páginas públicas.

- [ ] **Otimizar queries N+1** com `select_related` / `prefetch_related` nas views públicas
  - Conferir `apps/catalog/views.py`
  - Já feito em `apps/orders/views.py:checkout_success` (`.prefetch_related('items__variant__product')`)

- [ ] **CDN na frente** (Cloudflare grátis basta)
  Reduz latência geográfica e absorve tráfego DDoS antes do servidor.

- [ ] **Otimização de imagens** — todos os PNGs grandes em `media/products/featured/` (alguns chegam a 2 MB).
  Considerar: rodar `pip install pillow` + script que gera thumbnails ou converte para WebP.

- [ ] **Pre-compute totais pesados** — se aparecer relatórios admin lentos, materializar em `OrderStats` model atualizado por signal.

- [ ] **Pool de conexões dedicado** — PgBouncer se passar de ~20 req/s sustentado (sinal: `pg_stat_activity` mostrando muitas conexões).

---

## 🛠️ INFRAESTRUTURA

- [ ] **Servidor / hospedagem contratado** (VPS ou PaaS)
- [ ] **Domínio apontado** (DNS A → IP do servidor)
- [ ] **Certificado HTTPS** (Let's Encrypt via certbot, ou Cloudflare proxied)
- [ ] **Banco Postgres** provisionado em prod (separado do de dev!)
- [ ] **Variáveis de ambiente** preenchidas (`.env` de prod conferido com `.env.example`)
- [ ] **`python manage.py migrate`** rodado em prod
- [ ] **`python manage.py collectstatic`** rodado em prod
- [ ] **`python manage.py createsuperuser`** rodado em prod (com senha forte!)
- [ ] **Gunicorn rodando** (systemd: `systemctl status ngdsite`)
- [ ] **nginx rodando** (`systemctl status nginx`)
- [ ] **Logs sendo gravados** em `logs/ngdsite.log`
- [ ] **Backup do banco** configurado em cron diário

Ver passo a passo em [deploy/DEPLOY.md](deploy/DEPLOY.md).

---

## 📊 OBSERVABILIDADE

- [ ] **Sentry** para erros 500
  ```bash
  pip install sentry-sdk[django]
  ```
  Adicionar 6 linhas no `setup/settings.py` ([guia oficial](https://docs.sentry.io/platforms/python/integrations/django/)).
  Crítico — sem isso você não sabe quando algo quebra para o cliente.

- [ ] **UptimeRobot** ou similar — ping de `/healthz` a cada 5 min

- [ ] **Notificação de pedido pago** chegando no Telegram (já implementado, só testar em prod)

- [ ] **Notificação de erro de webhook** — adicionar Sentry breadcrumb no try/except do webhook MP

- [ ] **Dashboard de pedidos** (kanban já existe em `/admin/kanban/`) — confirmar que carrega rápido com 100+ pedidos

---

## 🧪 TESTES

> Sem testes automatizados, qualquer mudança futura tem risco de regressão.
> Não é bloqueante para lançar, mas é altamente recomendado antes da primeira versão estável.

- [ ] **Setup de pytest-django**
  ```bash
  pip install pytest pytest-django factory-boy
  ```
- [ ] **Testes do checkout** (cenários):
  - [ ] Carrinho vazio redireciona pra home
  - [ ] Quantidade negativa é clampada para 1
  - [ ] Preço enviado pelo cliente é ignorado (recalcula do banco)
  - [ ] Frete inválido é rejeitado
  - [ ] Variant inativa rejeita o pedido
  - [ ] Pedido é criado atomicamente (mock falha em OrderItem.create → Order não persiste)

- [ ] **Testes do webhook MP**:
  - [ ] Sem assinatura em prod → 401
  - [ ] Assinatura inválida → 401
  - [ ] Assinatura válida + valor menor que total → ignora
  - [ ] Assinatura válida + valor correto → marca pedido como pago
  - [ ] Replay (mesmo payment_id) → idempotente

- [ ] **Testes de upload**:
  - [ ] PDF válido passa
  - [ ] `.exe` renomeado para `.pdf` é rejeitado por magic bytes
  - [ ] Arquivo > 50 MB rejeitado
  - [ ] Path traversal (`../../etc/passwd`) sanitizado

- [ ] **Testes de propriedade do pedido**:
  - [ ] Usuário A não vê pedido do usuário B
  - [ ] Sessão sem flag verificada não consegue gerenciar arte

- [ ] **Smoke test em CI** (GitHub Actions): `manage.py check` + `pytest`

---

## 📋 COMANDOS RÁPIDOS

### Desenvolvimento
```bash
# Subir o servidor de dev
venv/Scripts/python.exe manage.py runserver

# OU pelo .bat já existente
run_ngd.bat

# Migrations após mudar models
venv/Scripts/python.exe manage.py makemigrations
venv/Scripts/python.exe manage.py migrate

# Gerar SECRET_KEY nova
venv/Scripts/python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Conferir saúde da configuração
venv/Scripts/python.exe manage.py check
venv/Scripts/python.exe manage.py check --deploy
```

### Produção (Linux)
```bash
# Atualizar código + dependências
git pull
venv/bin/pip install -r requirements.txt

# Rodar migrations
venv/bin/python manage.py migrate --noinput
venv/bin/python manage.py collectstatic --noinput

# Reiniciar
sudo systemctl restart ngdsite
sudo systemctl status ngdsite

# Ver logs
sudo journalctl -u ngdsite -f
tail -f logs/ngdsite.log
```

### Backup do Postgres
```bash
# Manual
pg_dump -U ngdsite -h localhost ngdsite | gzip > backup-$(date +%Y%m%d).sql.gz

# Cron diário (às 3h da manhã, mantém 7 dias)
0 3 * * * pg_dump -U ngdsite ngdsite | gzip > /var/backups/ngd/$(date +\%Y\%m\%d).sql.gz && find /var/backups/ngd/ -name '*.sql.gz' -mtime +7 -delete
```

---

## 🐛 TROUBLESHOOTING

### "RuntimeError: SECRET_KEY ausente"
Faltou setar `SECRET_KEY` no `.env`. Gere uma nova com o comando da seção "Comandos rápidos".

### "RuntimeError: ALLOWED_HOSTS não configurado"
Em prod, é obrigatório setar o domínio real em `ALLOWED_HOSTS=` no `.env`.

### Webhook MP retornando 401 em prod
Faltou setar `MP_WEBHOOK_SECRET`, ou o secret no painel do MP é diferente do `.env`.

### Cliente reclama que pagou mas pedido continua "aguardando_pagamento"
Possíveis causas:
1. Webhook não está recebendo (firewall? URL errada no painel MP?)
2. `MP_WEBHOOK_SECRET` errado → webhook é rejeitado com 401 (ver `logs/ngdsite.log`)
3. Valor pago menor que total (cliente fez parcial?) → rejeitado intencionalmente

### Performance ruim
1. Rodar `EXPLAIN ANALYZE` nas queries lentas (ativar `django-debug-toolbar` em dev)
2. Verificar `pg_stat_activity` por queries pendentes
3. Subir `GUNICORN_WORKERS` (mais CPU = mais workers)
4. Ativar Redis (`REDIS_URL`)

### Upload de arte rejeitado mesmo sendo arquivo válido
Conferir se o arquivo bate com a extensão (PDF de verdade começa com `%PDF-`). Se for um caso legítimo (CDR antigo sem header padrão), ajustar `ART_MAGIC_BYTES` em `apps/orders/views.py`.

---

## 🔗 LINKS ÚTEIS

- [Painel Mercado Pago](https://www.mercadopago.com.br/developers/panel/app)
- [Documentação Django Security](https://docs.djangoproject.com/en/5.2/topics/security/)
- [django-allauth docs](https://docs.allauth.org/)
- [django-ratelimit docs](https://django-ratelimit.readthedocs.io/)
- [WhiteNoise docs](https://whitenoise.readthedocs.io/)
- [Sentry Django integration](https://docs.sentry.io/platforms/python/integrations/django/)
- Auditoria de segurança detalhada: este arquivo + comentários inline no código

---

## 📝 HISTÓRICO DE MUDANÇAS DESTE ARQUIVO

| Data | Resumo |
|---|---|
| 2026-05-04 | Documento criado após hardening completo (settings, webhook HMAC, checkout atomic, validação de upload, rate limiting, artefatos de deploy) |
