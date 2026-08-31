# Tarefa: ligar o catálogo NGD ao Supabase

Este arquivo é o roteiro da tarefa. Leia inteiro antes de começar.

---

## Contexto

A NGD tem **dois sites diferentes**, e confundir os dois quebra o negócio:

| | Onde fica | O que é |
|---|---|---|
| **Site oficial** | `C:\projetos\nucleografico` | **JÁ ESTÁ NO AR** em nucleografico.com.br. SPA React + Vite no Firebase Hosting, backend no Supabase. 38 páginas indexadas no Google. |
| **Catálogo novo** | `C:\projetos\NGDPORTFOLIO` | Django. Ainda **não** está no ar. É onde você vai trabalhar. |

O plano é servir o catálogo em `nucleografico.com.br/loja`, através de um rewrite
do Firebase para o Cloud Run. Subpasta, e não domínio separado, para aproveitar a
autoridade que o domínio já tem no Google.

Todo o código do Django já está pronto e testado. **Falta apenas conectar ao
Supabase.** É isso que esta tarefa faz.

---

## Regras que não podem ser quebradas

1. **Não altere nada em `C:\projetos\nucleografico`.** Nem um arquivo. Aquele é
   o site que está no ar e dá dinheiro. Leitura é permitida; escrita não.
2. **Não rode `firebase deploy`.** Nenhuma variação, nem preview. Não faz parte
   desta tarefa.
3. **Não toque no schema `public` do Supabase.** É onde vivem as tabelas do site
   (`blog_posts`, `services`, `portfolio_items`, `hero_slides`, `clients`,
   `contact_submissions`). O catálogo vai para um schema separado.
4. **Não use os buckets `blog`, `carousel`, `client-logos`,
   `contact-attachments` nem `resumes`.** São do site. O catálogo tem bucket
   próprio.
5. **Migrations rodam pela conexão direta (porta 5432), nunca pelo pooler
   (6543).** O pooler em modo transação não foi feito para comandos de estrutura.

Se algo não estiver claro, **pergunte antes de agir**. Um erro aqui derruba um
site que fatura.

---

## O que você precisa pedir ao usuário

Nada disso existe na máquina. Peça:

1. A **senha** escolhida para o usuário de banco `django_catalogo`.
2. O **host do pooler** do Supabase — Project Settings > Database > Connection
   pooling.
3. As **chaves S3** do Storage — Project Settings > Storage > S3 Connection
   (access key id e secret access key).
4. Confirmação de que o **bucket `catalogo` já foi criado e é público**. Só o
   usuário consegue criar, pelo painel. Se ainda não existir, peça que crie:
   Storage > New bucket > nome `catalogo` > marcar Public.

O projeto Supabase é `eisqwuikemthtebpdqbj` — o mesmo do site. O isolamento vem
do schema e do bucket, não de um projeto separado.

---

## Passo a passo

Trabalhe sempre em `C:\projetos\NGDPORTFOLIO`. O Python é `./venv/Scripts/python.exe`.

### 1. Rodar o SQL no Supabase

O arquivo `deploy/supabase-catalogo.sql` já está pronto. Ele cria o schema
`catalogo`, o usuário `django_catalogo` e — o mais importante — os `REVOKE` que
impedem esse usuário de alcançar qualquer tabela do site.

Troque `TROQUE_ESTA_SENHA` pela senha que o usuário passou. O SQL é colado no
SQL Editor do painel do Supabase, por uma pessoa. Você não tem acesso ao painel.

O script termina com duas conferências. A segunda **precisa voltar vazia** — é a
prova de que o isolamento funcionou. Peça o resultado ao usuário.

### 2. Preencher o `.env`

O arquivo `.env.example` já traz o bloco pronto e comentado. Copie de lá para o
`.env` e preencha:

```
DB_NAME=postgres
DB_USER=django_catalogo.eisqwuikemthtebpdqbj
DB_PASSWORD=<a senha>
DB_HOST=aws-1-us-west-2.pooler.supabase.com
DB_PORT=6543
DB_SCHEMA=catalogo
DB_SSLMODE=require
DB_POOLER=True

SUPABASE_S3_ENDPOINT=https://eisqwuikemthtebpdqbj.supabase.co/storage/v1/s3
# us-west-2, NAO sa-east-1. Verificado em 31/08/2026 pela faixa de IP da AWS.
# Com a regiao errada o upload das imagens falha.
SUPABASE_S3_REGION=us-west-2
SUPABASE_S3_ACCESS_KEY_ID=<access key>
SUPABASE_S3_SECRET_ACCESS_KEY=<secret key>
SUPABASE_STORAGE_BUCKET=catalogo
```

**Atenção ao `DB_USER`:** no pooler do Supabase o usuário leva o id do projeto
colado com um ponto. `django_catalogo` sozinho não conecta.

### 3. Criar as tabelas

Pela **conexão direta**, não pelo pooler. Para este comando use `DB_PORT=5432`,
o host direto (`db.eisqwuikemthtebpdqbj.supabase.co`) e `DB_USER=django_catalogo`
sem o sufixo:

    python manage.py migrate

Depois volte o `.env` para os valores do pooler.

### 4. Conferir

    python manage.py checar_supabase

Este comando existe justamente para isto. Ele verifica três coisas:

1. a conexão e em qual schema as tabelas foram criadas;
2. que o catálogo **não consegue** ler as tabelas do site — se ele conseguir,
   PARE e avise, algo saiu errado no SQL;
3. que dá para gravar, ler e apagar um arquivo no bucket.

**Só siga adiante com os três verdes.**

### 5. Levar as imagens

    python manage.py migrar_media_supabase --simular
    python manage.py migrar_media_supabase

São 210 arquivos, cerca de 140 MB. O comando **não envia** `media/uploads/` por
padrão: são arquivos enviados por clientes e o bucket é público. Não use
`--incluir-uploads`.

### 6. Conferir que o site continua de pé

    python manage.py check
    python manage.py runserver

Abra a home, três páginas de produto e a Quem Somos. As imagens devem carregar a
partir de uma URL como
`https://eisqwuikemthtebpdqbj.supabase.co/storage/v1/object/public/catalogo/...`

---

## Se der errado

Tudo aqui é reversível.

**Voltar o Django ao estado anterior:** esvazie as variáveis `SUPABASE_S3_*`,
`DB_SCHEMA`, `DB_SSLMODE` e `DB_POOLER` do `.env` e volte `DB_HOST=localhost`.
Sem essas variáveis o projeto usa o Postgres local e a pasta `media/`,
exatamente como antes. Não é preciso mexer em código.

**Desfazer o lado Supabase:**

```sql
drop schema catalogo cascade;
drop user django_catalogo;
```

E apagar o bucket `catalogo` no painel. O schema `public` e os buckets do site
não são afetados.

**Voltar o código:** o último commit bom é `32cc278`, na branch `portfolio`.

---

## Leitura de apoio

- `deploy/SUBPASTA-LOJA.md` — o runbook completo, incluindo o rewrite do
  Firebase e a ordem segura de publicação.
- `deploy/supabase-catalogo.sql` — o SQL desta tarefa.
- `.env.example` — todas as variáveis, comentadas.

---

## O que NÃO faz parte desta tarefa

Pare quando o `checar_supabase` estiver verde e as imagens tiverem subido. O
deploy no Cloud Run e o rewrite no Firebase são etapas seguintes, com aprovação
à parte. **Não avance sozinho até lá.**
