# Imagem do catálogo NGD para o Cloud Run.
#
# Construída por:  gcloud run deploy ngd-loja --source .
# O serviço resultante é o alvo do rewrite /loja/** no firebase.json do site
# oficial. Ver deploy/SUBPASTA-LOJA.md.
#
# Nada aqui toca no site que já está no ar: este contêiner responde apenas
# pelo que o Firebase Hosting encaminhar para /loja/**.

FROM python:3.12-slim

# Logs sem buffer (aparecem na hora no Cloud Logging) e sem .pyc no disco
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependências primeiro: esta camada só é reconstruída quando requirements.txt
# muda, o que deixa os deploys seguintes bem mais rápidos.
# psycopg2-binary e Pillow vêm com wheels prontas, então não é preciso
# compilador nem biblioteca de sistema.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Estáticos empacotados na imagem, com hash e compressão, servidos pelo
# WhiteNoise. As variáveis abaixo existem só nesta camada de build: o
# collectstatic exige SECRET_KEY e ALLOWED_HOSTS preenchidos quando DEBUG=False,
# mas nenhuma delas vale em tempo de execução — em produção valem as variáveis
# de ambiente do próprio Cloud Run.
RUN SECRET_KEY=build-only-nao-usada-em-runtime \
    DEBUG=False \
    ALLOWED_HOSTS=build.invalid \
    SITE_URL=https://build.invalid \
    python manage.py collectstatic --noinput

# O Cloud Run injeta a porta em PORT; gunicorn.conf.py já lê essa variável.
CMD ["gunicorn", "-c", "gunicorn.conf.py", "setup.wsgi:application"]
