# Catálogo NGD em nucleografico.com.br/loja

Como colocar este projeto Django numa subpasta do site oficial **sem tocar no
site que já está no ar**. O site atual (SPA no Firebase Hosting) continua
servindo todas as rotas de hoje; só `/loja/**` passa a cair no Django.

Regra que guiou este documento: **nada aqui é irreversível.** Cada etapa tem
como voltar, e a ordem abaixo é a que mantém o site no ar o tempo todo.

---

## 1. Como funciona

O Firebase Hosting sozinho não roda Django (ele só entrega arquivo pronto).
Mas ele sabe encaminhar uma rota para um contêiner no Cloud Run. Então:

    nucleografico.com.br/          -> SPA de hoje          (nada muda)
    nucleografico.com.br/lp/...    -> SPA de hoje          (nada muda)
    nucleografico.com.br/loja/**   -> Django no Cloud Run  (novo)

Sem mexer em DNS, sem domínio novo, sem Cloudflare.

---

## 2. O rewrite no firebase.json

O site atual vive em `C:\projetos\nucleografico\Github` (Vite + React, publicado
a partir de `dist/`). Projeto Firebase: `ngd-nucleografico-e074e`.

Hoje o `firebase.json` termina assim:

```json
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
```

A alteração é **acrescentar um bloco antes**, sem tirar nada:

```json
    "rewrites": [
      {
        "source": "/loja/**",
        "run": { "serviceId": "ngd-loja", "region": "southamerica-east1" }
      },
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
```

**A ordem importa.** A regra do `/loja/**` tem que vir ANTES do `"**"` do SPA.
Se ficar depois, o SPA engole tudo e o catálogo nunca aparece.

Os 10 redirecionamentos 301 que já existem em `redirects` **não são tocados**.
Eles rodam antes dos rewrites e continuam funcionando igual.

Confirmar no console que `southamerica-east1` está na lista de regiões que o
Firebase Hosting aceita para rewrite de Cloud Run; se não estiver, usar a
região suportada mais próxima. Só isso muda no arquivo.

Não há colisão de rotas: o admin do SPA é `/admin`, o do Django passa a ser
`/loja/admin/`. E o blog já existe no site atual (`/blog`, com automação
própria em `06_blog_automacao`) — o catálogo **não** deve criar um segundo blog.

---

## 3. O que precisa estar resolvido antes

- **`SCRIPT_NAME=/loja` no `.env`.** Já implementado em `setup/settings.py`:
  liga o prefixo em links, canonical, sitemap, static e media. Testado nos dois
  cenários (raiz e `/loja`).
- **Banco e imagens no Supabase, no mesmo padrão do site.** Ver a seção 3.1
  logo abaixo. O Django já está configurado; falta preencher o `.env`.
  Lembrete do porquê: o disco do Cloud Run é efêmero, então toda imagem enviada
  pelo admin sumiria no deploy seguinte se ficasse no contêiner. **É o item que
  quebra o catálogo se for esquecido.**
- **`ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`** com `nucleografico.com.br`.
- **Sitemap pelo Search Console.** O `robots.txt` só vale na raiz do domínio, e
  a raiz é do site atual, que não vamos tocar — ele já está ajustado no apex
  desde as correções de 18/08/2026 e tem 38 URLs. O
  `nucleografico.com.br/loja/sitemap.xml` entra **como um sitemap separado** em
  Sitemaps no GSC, sem mexer no que já está lá. A propriedade do GSC já cobre a
  subpasta, não precisa criar nada.

### 3.1 Supabase: schema e bucket próprios

O site oficial usa o projeto `eisqwuikemthtebpdqbj`. O catálogo entra **no mesmo
projeto**, seguindo o mesmo padrão, mas com espaço só dele: um schema próprio no
banco e um bucket próprio no Storage. Nada se mistura com o que já está no ar.

**Passo 1 — Storage.** Criar um bucket **público** chamado `catalogo`, do mesmo
jeito que `blog` e `carousel`. As pastas internas (`products/featured/`,
`products/gallery/`, `products/modelos/`, `categories/`) o Django cria sozinho.

**Passo 2 — Banco.** No SQL Editor do Supabase, rodar:

```sql
-- Espaço próprio do catálogo, dentro do mesmo banco
create schema if not exists catalogo;

-- Usuário do Django. Troque a senha antes de rodar.
create user django_catalogo with password 'TROQUE_ESTA_SENHA';

grant usage, create on schema catalogo to django_catalogo;
grant all privileges on all tables    in schema catalogo to django_catalogo;
grant all privileges on all sequences in schema catalogo to django_catalogo;
alter default privileges in schema catalogo grant all on tables    to django_catalogo;
alter default privileges in schema catalogo grant all on sequences to django_catalogo;

-- A trava: enxerga o schema public (por causa das extensões), mas não pode
-- criar nada lá nem tocar nas tabelas do site.
grant usage on schema public to django_catalogo;
revoke create on schema public from django_catalogo;
revoke all on all tables in schema public from django_catalogo;
```

É esse `revoke` que garante a separação de verdade: mesmo que uma migration do
Django saia errada, ela **não tem permissão** de encostar em `blog_posts`,
`services`, `portfolio_items` ou qualquer outra tabela do site.

**Passo 3 — `.env` do catálogo:**

```
# Banco (Connection Pooling, modo Transaction)
DB_NAME=postgres
DB_USER=django_catalogo.eisqwuikemthtebpdqbj
DB_PASSWORD=<a senha definida no SQL acima>
DB_HOST=<host do pooler, em Project Settings > Database>
DB_PORT=6543
DB_SCHEMA=catalogo
DB_SSLMODE=require
DB_POOLER=True

# Storage (Project Settings > Storage > S3 Connection)
SUPABASE_S3_ENDPOINT=https://eisqwuikemthtebpdqbj.supabase.co/storage/v1/s3
SUPABASE_S3_REGION=sa-east-1
SUPABASE_S3_ACCESS_KEY_ID=<access key>
SUPABASE_S3_SECRET_ACCESS_KEY=<secret key>
SUPABASE_STORAGE_BUCKET=catalogo
```

Dois detalhes que custam horas se passarem batido:

- No pooler do Supabase o usuário leva o id do projeto colado com um ponto:
  `django_catalogo.eisqwuikemthtebpdqbj`, não só `django_catalogo`.
- **Rodar as migrations pela conexão direta (porta 5432), não pelo pooler.**
  Depois que o banco estiver criado, aí sim o Cloud Run usa o pooler no dia a
  dia. O pooler em modo transação não foi feito para comandos de estrutura.

---

## 4. Reversão

Três níveis, do mais leve ao mais pesado.

### Testar sem afetar produção (usar sempre)

O Firebase publica em canal de preview: gera uma URL temporária com o rewrite
já valendo, e a produção não muda nada.

    firebase hosting:channel:deploy preview-loja --expires 7d

Só depois de aprovar nessa URL é que vai para produção.

### Desfazer um deploy que já foi para produção

Console do Firebase > Hosting > histórico de versões > **Reverter**. Volta a
versão anterior do site inteiro em segundos, incluindo o rewrite.
É por isso que o rewrite é seguro: ele é uma linha de configuração versionada,
não uma alteração no conteúdo do site.

### Desfazer o lado Supabase

```sql
drop schema catalogo cascade;
drop user django_catalogo;
```

E apagar o bucket `catalogo` no painel. Como tudo do catálogo vive dentro desse
schema e desse bucket, some sem deixar rastro — o schema `public` e os buckets
do site (`blog`, `carousel`, `client-logos`, `contact-attachments`, `resumes`)
não são tocados.

### Desfazer o lado Django

    git log --oneline          # achar o commit bom
    git reset --hard <commit>

Desligar o prefixo sem mexer em código: tirar `SCRIPT_NAME` do `.env` e
reiniciar. O site volta a responder na raiz.

---

## 5. Ordem segura

Os passos 1 a 5 não encostam no site: acontecem no Supabase, na sua máquina e
numa URL própria do Cloud Run. O Firebase só entra no passo 6.

**1. Criar o espaço no Supabase.** Bucket `catalogo` e o SQL da seção 3.1.

**2. Preencher o `.env`** com os valores da seção 3.1.

**3. Criar as tabelas** — pela conexão direta, porta 5432, nunca pelo pooler:

    python manage.py migrate

**4. Conferir se está tudo certo:**

    python manage.py checar_supabase

Confere a conexão, prova que o catálogo **não alcança** as tabelas do site e
grava/lê/apaga um arquivo no bucket. Só siga em frente com tudo verde.

**5. Levar as imagens e subir o contêiner:**

    python manage.py migrar_media_supabase --simular    # confira a lista
    python manage.py migrar_media_supabase              # envia
    gcloud run deploy ngd-loja --source .

Testar pela URL `...run.app` que o Cloud Run devolve. O site oficial continua
intocado até aqui.

**6. Rewrite em canal de preview:**

    firebase hosting:channel:deploy preview-loja --expires 7d

**7. Conferir na URL de preview:** home, três páginas de produto, Quem Somos,
`/loja/sitemap.xml`, imagens e CSS carregando.

**8. Publicar em produção** e enviar o sitemap no Search Console.

Se algo sair errado em qualquer ponto depois do passo 6, o botão Reverter do
Hosting devolve o estado anterior.

---

## 6. O que já está pronto no repositório

| Arquivo | Para que serve |
|---|---|
| `Dockerfile` | Imagem do Cloud Run. Instala as dependências, roda o `collectstatic` e sobe o Gunicorn na porta que o Cloud Run injeta. |
| `.dockerignore` | Mantém `.env`, `media/`, `venv/` e backups fora da imagem. |
| `gunicorn.conf.py` | Passou a respeitar a variável `PORT` do Cloud Run. |
| `setup/settings.py` | `SCRIPT_NAME` (subpasta), banco no Supabase (schema, SSL, pooler) e Storage no Supabase. Tudo por variável de ambiente. |
| `.env.example` | Modelo com todas as variáveis novas, comentadas. |
| `manage.py checar_supabase` | Confere banco, isolamento e Storage antes do deploy. |
| `manage.py migrar_media_supabase` | Leva `media/` para o bucket. Aceita `--simular`. |
| `manage.py renomear_imagens_seo` | Renomeia as imagens usando o slug do produto. Aceita `--simular` e `--desfazer`. |

Sobre o `renomear_imagens_seo`: os arquivos vinham com nomes como
`Gemini_Generated_Image_ngtxengtxengtxen.png`, que não dizem nada ao Google e
ainda anunciam que a imagem é gerada por IA. Passaram a se chamar
`totem-eliptico-em-poliondas.png`, `...-02.png` e assim por diante. Já foi
rodado uma vez (63 imagens); rodar de novo depois de cadastrar produto novo é
seguro, ele ignora o que já está certo. Cada execução grava o de/para em
`backups/`, e `--desfazer <mapa>` devolve os nomes antigos.

**Enquanto o `.env` não tiver as credenciais do Supabase, nada muda:** os
uploads continuam em `media/`, o banco continua o local e o site roda na raiz,
exatamente como hoje. Toda a configuração é liga-desliga por variável de
ambiente, sem alterar código.

Um detalhe do `migrar_media_supabase`: ele **não envia** `media/uploads/` por
padrão. São arquivos enviados por clientes e o bucket é público. Use
`--incluir-uploads` só se tiver certeza de que aquilo pode ficar acessível
por URL.
