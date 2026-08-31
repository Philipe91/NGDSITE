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
# us-west-2, NAO sa-east-1: com a regiao errada o upload falha
SUPABASE_S3_REGION=us-west-2
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

---

## 7. Execução — 31/08/2026

Esta seção é o registro do que foi **de fato executado**, com os valores reais
descobertos. As seções 1 a 6 são o plano; esta é a realidade, e onde as duas
divergirem, vale esta.

### 7.1 O que foi feito, em ordem

1. **Bucket `catalogo`** criado no Supabase, público, sem limite de tamanho nem
   restrição de MIME.
2. **SQL de isolamento executado** no SQL Editor: schema `catalogo`, usuário
   `django_catalogo`, grants no schema próprio e os três `revoke` no `public`.
   As duas consultas de conferência voltaram `1 row` (schema criado) e
   `0 rows` (nenhum privilégio no `public`) — o isolamento está provado.
3. **Chaves S3 criadas** (`catalogo-upload`). Não existiam antes; o painel
   mostra o secret **uma única vez**, na criação.
4. **210 imagens do portfolio** migradas para `catalogo` (209 subiram).
5. **Bucket `loja`** criado, e as **211 imagens do NGDSITE** migradas para ele
   (210 subiram). Buckets separados — ver 7.3.
6. **55 migrations aplicadas** no Postgres do Supabase, **pela conexão direta**
   (porta 5432), conforme a seção 3.1 manda. Resultado: 29 tabelas no schema
   `catalogo`, e o `django_catalogo` seguiu com **zero privilégio no `public`**
   depois de tudo.
7. **`FORCE_SCRIPT_NAME` implementado** e os 3 caminhos absolutos cravados
   trocados por `reverse` (commit `cfe5eb3`).
8. **`.env.production` preenchido** e validado: `manage.py check --deploy`
   passa com zero problemas.
9. **`gcloud` CLI instalada**, APIs habilitadas, `.gcloudignore` criado.

### 7.2 Valores reais (os que o plano deixou como `<preencher>`)

| Item | Valor |
|---|---|
| Projeto Supabase | `eisqwuikemthtebpdqbj`, região `us-west-2` |
| Host do pooler | `aws-1-us-west-2.pooler.supabase.com` porta 6543 |
| Host direto (migrations) | `db.eisqwuikemthtebpdqbj.supabase.co` porta 5432 |
| Projeto Google Cloud | `ngd-nucleografico-e074e`, plano **Blaze** |
| Conta com acesso | `ngd.growth@gmail.com` (é a `authuser=6` no Console) |
| Serviço Cloud Run | `ngd-loja`, região `us-west1` |
| Bucket do portfolio | `catalogo` |
| Bucket da loja (NGDSITE) | `loja` |

As credenciais ficam em `.env.production`, coberto pelo `.gitignore` (linha 34).
Nunca versionar.

### 7.3 Por que dois buckets, e não um

Os dois projetos têm **cerca de 154 arquivos com o mesmo nome e conteúdo
diferente** — o portfolio passou pelo `renomear_imagens_seo` e o NGDSITE não.
Como o storage grava com `file_overwrite: True`, um bucket só faria um projeto
apagar as imagens do outro. Daí `catalogo` para o portfolio e `loja` para o
NGDSITE.

### 7.4 Sete armadilhas que custaram tempo

1. **O endpoint do S3 é `<ref>.supabase.co`, não `<ref>.storage.supabase.co`.**
   O painel exibe a segunda forma, mas o `settings.py` deriva a URL pública do
   endpoint (`split("/storage/v1")[0]`) para bater com o `getPublicUrl()` do
   site. Trocar o host manda as imagens para um endereço diferente do resto do
   site. **O que o painel mostra não é o que este projeto precisa.**

2. **O host do pooler é `aws-1`, não `aws-0`.** Não dá para deduzir a partir da
   região. Se a dashboard do Supabase estiver fora do ar (aconteceu), descubra
   testando: host errado responde `(ENOTFOUND) tenant/user ... not found`, host
   certo autentica.

3. **A conexão direta é só IPv6.** O Cloud Run sai por IPv4, então em produção
   **o pooler é obrigatório** — a conexão direta serve para as migrations
   rodadas da máquina local.

4. **O pooler em modo transação preserva o `search_path`.** Isso foi testado:
   `current_schema()` volta `catalogo` e o ORM lê do lugar certo. Era a dúvida
   que justificava rodar as migrations pela conexão direta.

5. **O Cloud Run não executa a fase `release:` do `Procfile`.** Isso é coisa de
   Heroku. Migrations e `collectstatic` precisam ser resolvidos por fora — aqui,
   as migrations foram rodadas à mão e o `collectstatic` está no `Dockerfile`
   (linha 36).

6. **Arquivo com acento no nome falha no upload S3.** O
   `megamenu/totens/totem_eliptico.png` (com acento no "i") dá `HeadObject 400`
   nos dois projetos. É órfão — nenhum banco o referencia; o arquivo usado é o
   `totem_elipticocapa.png`. Se aparecer outro caso, renomear para ASCII.

7. **`workers = cpu*2+1` estoura a memória padrão do Cloud Run.** Numa vCPU dá
   3 processos Django, uns 200 MB cada. Fixado `GUNICORN_WORKERS=2` com 1 GB.

### 7.5 Como refazer o deploy

Da pasta `NGDPORTFOLIO`, com o `gcloud` já autenticado:

```
gcloud run deploy ngd-loja --source . --region us-west1 --allow-unauthenticated --env-vars-file <caminho do env.yaml> --memory 1Gi --cpu 1 --quiet
```

O `env.yaml` é o `.env.production` convertido para YAML (uma linha
`CHAVE: "valor"` por variável), mais `GUNICORN_WORKERS: "2"`. Como contém
segredos, gere num diretório temporário e apague depois — não deixe no repo.

O `.gcloudignore` é obrigatório: sem ele o upload sobe **1,1 GB**
(`venv` 808 MB + `media` 148 MB + `.git` 97 MB) em vez de ~365 arquivos.

**Testar sempre pela URL do Cloud Run antes de mexer no domínio.** Como o
`FORCE_SCRIPT_NAME` é `/loja`, o endereço de teste tem o sufixo:
`https://ngd-loja-XXXX.run.app/loja/` — a raiz dá 404, e isso é o esperado.

### 7.6 O que ainda falta

- O **rewrite `/loja/**` no `firebase.json`** do site no ar. Precisa vir
  **antes** do catch-all `"source": "**"`, porque o Firebase resolve rewrites
  em ordem e o primeiro que casa vence. Sendo aditivo e anterior, nenhuma rota
  atual muda de comportamento. É o **único passo que encosta no site publicado**.
- As **rotações de credencial** do `PRODUCAO.md` (Mercado Pago, Gmail, Telegram,
  senha do Postgres local). Como esta subida é a versão enxugada
  (`PORTFOLIO_MODE=True`, sem carrinho nem pagamento), o token do Mercado Pago
  não bloqueia **esta** subida — vira bloqueio quando a loja com venda subir.
- Trocar a senha do `django_catalogo`, que ficou exposta na transcrição da
  sessão em que foi criada. Combinado para quando o site passar a vender.

### 7.7 Nota de segurança

A chave S3 do Supabase **dá acesso a todos os buckets do projeto e ignora as
policies de RLS** — o próprio painel avisa isso na criação, e não há opção de
restringir por bucket. O isolamento que existe é o do **banco**, não o do
storage. Consequência prática: essa chave só pode viver em `.env.production` e
nas variáveis do Cloud Run, nunca no Git nem numa imagem de container.

### 7.8 Armadilha nº 8 — a que só apareceu no deploy de teste

**`FORCE_SCRIPT_NAME` resolve apenas metade do subcaminho.** Ele faz o Django
*gerar* os links com o prefixo, mas não muda como o Django *interpreta* o
caminho que chega — a resolução de URL usa `PATH_INFO` cru.

Sintoma no primeiro deploy: a home respondia em `/` com 26 links apontando para
`/loja/...`, e o CSS em `/loja/static/...` dava **404** enquanto `/static/...`
dava 200. A página montava apontando para endereços que ela mesma não atendia.

Atrás do Firebase seria pior, porque o rewrite encaminha o **caminho completo**
(`/loja/categoria/x`) para o Cloud Run.

A correção está em `setup/wsgi.py`: um wrapper WSGI move o prefixo de
`PATH_INFO` para `SCRIPT_NAME`, que é o lugar certo dele. Aceita os dois
formatos — com prefixo (Firebase) e sem (URL direta do Cloud Run, para teste).

**Lição:** o `check --deploy` passa, o `reverse()` devolve o caminho certo e
mesmo assim o site quebra. Só um deploy de teste real, pela URL do Cloud Run,
revela isso — por isso o passo de testar em `*.run.app` antes de tocar no
`firebase.json` não é opcional.

### 7.9 Armadilha nº 9 — migration cria estrutura, não conteúdo

Depois do segundo deploy o site respondia 200 em `/loja/`, com o CSS correto —
mas **sem nenhum produto**, e `/loja/categoria/<slug>/` dava 404. As 55
migrations criaram as 29 tabelas **vazias**; o conteúdo continuava só no
Postgres local.

A carga foi feita com `dumpdata` no local e `loaddata` na produção, com dois
cuidados que importam:

1. **Encoding.** No Windows, `dumpdata -o arquivo.json` grava em cp1252 e o
   `loaddata` quebra com `UnicodeDecodeError`. Use
   `PYTHONIOENCODING=utf-8 ... dumpdata ... > arquivo.json` (redirecionando a
   saída, não com `-o`).

2. **Filtrar o que sobe.** O dump completo trazia **8 pedidos e 10 itens de
   teste**, 4 usuários com hash de senha de desenvolvimento (incluindo
   superusers), 3 e-mails e 1 perfil de cliente. Nada disso pode ir para
   produção — o `PRODUCAO.md` inclusive manda remover pedidos e usuários de
   teste. Subiram só os 125 objetos de conteúdo:

   | Entra | Fica de fora |
   |---|---|
   | `catalog.*` (111) | `orders.order`, `orders.orderitem` (18) |
   | `pages.page` (6) | `auth.user` (4) |
   | `sites.site`, `seo.seoconfig`, `orders.shippingconfig` | `account.emailaddress`, `customers.customerprofile` (4) |

   Além de `contenttypes`, `auth.Permission`, `sessions` e `admin.logentry`, que
   as migrations já recriam e causariam conflito de chave.

3. **Carga pela conexão direta**, não pelo pooler — mesma razão das migrations.

**Consequência:** como `auth.user` não subiu, **não existe superusuário em
produção**. Criar um com `createsuperuser` apontando para o `.env.production`
antes de precisar do admin.

### 7.10 Armadilha nº 10 — o service worker do PWA engole o /loja

**A pior do dia, porque era invisível para o `curl`.**

Depois do primeiro deploy no domínio, todos os testes por linha de comando
davam 200: `/loja/`, `/loja`, categorias, CSS, e os 10 redirects de SEO
intactos. No navegador, porém, aparecia a mensagem *"o serviço que você procura
não existe"* — que é do **React do site institucional**, não do Django.

**Causa:** o site é um PWA. O `vite.config.ts` tinha

```js
navigateFallback: "index.html",
navigateFallbackDenylist: [/^\/api/, /^\/supabase/],
```

O service worker intercepta **toda navegação** e serve o `index.html` do cache.
Como `/loja` não estava na lista de exceções, o pedido nunca chegava ao Firebase
— logo, nunca chegava ao Cloud Run. O React recebia uma rota que não conhece e
mostrava o "não encontrado" dele.

**Correção:** acrescentar `/^\/loja/` ao `navigateFallbackDenylist`, rebuildar e
republicar. Confirmar no arquivo publicado:

```
curl -s https://nucleografico.com.br/sw.js | grep -o "denylist:\[[^]]*\]"
→ denylist:[/^\/api/,/^\/supabase/,/^\/loja/]
```

**Duas lições:**

1. **`curl` não executa service worker.** Qualquer verificação de site com PWA
   feita só por linha de comando tem esse ponto cego. Testar em **janela
   anônima**, que não tem SW instalado e mostra o que um visitante novo vê.
2. Depois de corrigir, quem já visitou o site continua com o **SW antigo
   instalado** até ele se atualizar. `registerType: "autoUpdate"` resolve
   sozinho, mas costuma exigir uma visita a mais ou `Ctrl+Shift+R`.

---

## 8. Estado no fim de 31/08/2026

**No ar e funcionando:** https://nucleografico.com.br/loja/

Site institucional intacto (mesmo título e tamanho de antes), os 10 redirects de
SEO respondendo 301, e a loja servindo `/loja/`, `/loja` sem barra, categorias,
produtos e CSS.

### 8.1 Três arquivos alterados e NÃO COMMITADOS

Em `C:/projetos/nucleografico/Github`, branch `fix/seo-canonical-apex`:

| Arquivo | O que é | Já publicado? |
|---|---|---|
| `firebase.json` | os 14 inserts do rewrite `/loja` | **sim** |
| `vite.config.ts` | `/loja` na denylist do service worker | **sim** |
| `public/sitemap.xml` | trabalho do dono (posts do blog) | **não**, e foi mantido fora de propósito |

**Risco:** os dois primeiros estão publicados mas não versionados. Um
`git checkout` ou troca de branch os desfaz, e o próximo `firebase deploy`
quebraria o `/loja` silenciosamente. **Commitar assim que revisar.**

O `sitemap.xml` foi preservado com `git stash` nos dois deploys, por pedido
explícito do dono ("não mexa no lance do blog"), e devolvido intacto depois.

### 8.2 O que fazer amanhã

1. **Commitar** o `firebase.json` e o `vite.config.ts` (ver 8.1).
2. **Criar o superusuário** de produção — não existe nenhum, porque os 4
   usuários de teste foram deixados de fora de propósito:
   `createsuperuser` apontando para o `.env.production`.
3. **Conferir a loja no navegador** com calma: layout, imagens, menus, e se o
   carrinho está mesmo escondido (`PORTFOLIO_MODE=True`).
4. **Rotações de credencial** do `PRODUCAO.md` (Mercado Pago, Gmail, Telegram,
   senha do Postgres local) e a troca da senha do `django_catalogo`.
5. Só depois: subir a **versão que vende** (NGDSITE), cujo bucket `loja` já está
   migrado e cujo código já tem o bloco de storage.

### 8.3 Padrão de erro que se repetiu (para não repetir amanhã)

Três vezes no mesmo dia o erro foi **deduzir em vez de verificar**: o endpoint do
S3 (o painel mostra uma forma, o projeto precisa de outra), o host do pooler
(`aws-1`, não `aws-0`) e a URL de download do `gcloud` (faltava `/downloads/`).
Nos três casos o custo foi baixo porque houve teste antes de aplicar — mas os
três eram evitáveis lendo a fonte em vez de supor.

E duas vezes uma dificuldade foi declarada "bloqueio" cedo demais (acesso ao
Google Cloud, host do pooler) quando era só falta de insistir. As duas caíram
assim que houve mais uma tentativa.
