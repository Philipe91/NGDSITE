# Execução da ligação ao Supabase — registro

Companion de `PROMPT-SUPABASE.md` (o roteiro) e `SUBPASTA-LOJA.md` (o runbook).
Este arquivo registra **o que já foi feito**, **o que foi descoberto** e
**o que só você consegue fazer**.

Data: 31/08/2026 · Branch `portfolio` · commit base `32cc278`

---

## Estado atual: preparado, inativo, seguro

O `.env` já tem o bloco Supabase, mas **desligado**. Hoje o Django continua
usando Postgres local e a pasta `media/` — verificado:

    DB HOST/PORT : localhost 5432
    STORAGE      : django.core.files.storage.FileSystemStorage
    MEDIA_URL    : /media/
    manage.py check -> System check identified no issues

Nada no site que está no ar (`nucleografico.com.br`) foi tocado. Nenhum arquivo
de `C:\projetos\nucleografico` foi alterado. Nenhum `firebase deploy` foi rodado.

---

## Descobertas do pré-voo

Três coisas que o roteiro não sabia. A primeira era um bug que teria quebrado o
Storage na hora do upload.

### 1. O projeto fica em `us-west-2`, não em `sa-east-1`

O `.env.example` trazia `SUPABASE_S3_REGION=sa-east-1`. Está errado.

Como foi verificado, sem depender do painel: `db.eisqwuikemthtebpdqbj.supabase.co`
resolve para o IPv6 `2600:1f13:838:6e59::`, e essa faixa pertence a `us-west-2`
pela tabela oficial `ip-ranges.amazonaws.com`. Confirmado depois pelo pooler
(ver item 2).

Corrigido em `.env.example` e já aplicado no `.env`.

### 2. O pooler do projeto é `aws-1-us-west-2.pooler.supabase.com`

Descoberto sondando os endpoints regionais com uma senha propositalmente
inválida: o pooler errado responde `ENOTFOUND tenant/user`, o certo responde
erro de senha. Só `aws-1-us-west-2` reconheceu o tenant, nas duas portas:

| Endpoint | Porta | Resultado |
|---|---|---|
| `aws-0-sa-east-1` | 5432 | tenant não existe |
| `aws-1-sa-east-1` | 5432 | tenant não existe |
| `aws-0-us-west-2` | 5432 / 6543 | tenant não existe |
| **`aws-1-us-west-2`** | **5432 / 6543** | **tenant reconhecido** |

Isso gerou algumas tentativas de login recusadas no log do projeto. Não altera
nem lê nada.

### 3. As migrations vão rodar — a conexão direta responde

O host direto só tem registro IPv6 (não tem IPv4), o que costuma travar o passo
das migrations. Mas esta máquina tem IPv6 funcionando (16 ms até o Google), e o
TCP para `db.eisqwuikemthtebpdqbj.supabase.co:5432` abre normalmente por IPv6.

Se um dia isso falhar, o plano B é o **Session Pooler**
(`aws-1-us-west-2.pooler.supabase.com:5432`, usuário com o sufixo
`.eisqwuikemthtebpdqbj`), que aceita DDL. Quem não aceita é o Transaction
Pooler da 6543.

---

## Verificado que já está pronto

- `apps/core/management/commands/checar_supabase.py` e `migrar_media_supabase.py` existem
- `setup/settings.py` lê `DB_SCHEMA`, `DB_SSLMODE`, `DB_POOLER` e `SUPABASE_S3_*` (linhas 208-304)
- `boto3 1.43.83` e `django-storages` instalados no venv
- `.env` está no `.gitignore` (linha 32) e fora do índice do Git — seguro para senha
- `migrar_media_supabase --simular` → **210 arquivos**, já excluindo os 6 de
  `media/uploads/` (o roteiro dizia 211; a contagem real é 210)

---

## O que só você consegue fazer

São três coisas, todas no painel do Supabase. Eu não tenho acesso a ele, e a
senha de superusuário do banco não existe nesta máquina — por isso não dá para
automatizar. **A senha do `django_catalogo` eu já gerei** (40 caracteres,
aleatória); ela está no `.env`, nas linhas comentadas, e no SQL preenchido.

### Passo A — rodar o SQL

Peça a mim o arquivo `supabase-catalogo-PREENCHIDO.sql` (está fora do repo, para
a senha não ir parar no Git). Cole no **SQL Editor > New query > Run**.

Ele cria o schema `catalogo` e o usuário `django_catalogo`, e aplica os `REVOKE`
que impedem esse usuário de alcançar as tabelas do site. Não altera o schema
`public`.

O script termina com duas conferências. **Me mande o resultado das duas.**
A segunda tem que voltar **zero linhas** — é a prova do isolamento. Se voltar
qualquer linha, pare: algo saiu errado.

### Passo B — criar o bucket

**Storage > New bucket** → nome exatamente `catalogo` → marcar **Public** → criar.

Não use os buckets do site (`blog`, `carousel`, `client-logos`,
`contact-attachments`, `resumes`).

### Passo C — pegar as chaves S3

**Project Settings > Storage > S3 Connection** → gerar/copiar o *access key id* e
o *secret access key*. Me mande os dois.

---

## O que eu faço depois que você mandar

1. Ativo o bloco no `.env` (banco pelo pooler + as duas chaves S3)
2. Rodo `migrate` pela conexão direta (porta 5432, usuário sem sufixo) e devolvo
   o `.env` para o pooler
3. Rodo `checar_supabase` e só sigo com os **três verdes** — em especial o
   segundo, que confirma que o catálogo não lê as tabelas do site
4. Rodo `migrar_media_supabase` (210 arquivos, ~148 MB, sem `--incluir-uploads`)
5. Subo o servidor e confiro home, três páginas de produto e Quem Somos

Paro aí. Cloud Run e rewrite do Firebase são etapas seguintes, com aprovação à
parte.

---

## Se der errado

**Django volta ao estado anterior** esvaziando `SUPABASE_S3_ACCESS_KEY_ID`,
`SUPABASE_S3_SECRET_ACCESS_KEY`, `DB_SCHEMA`, `DB_SSLMODE`, `DB_POOLER` e
recomentando as linhas `DB_*` do Supabase. Sem código para mexer.

**Lado Supabase:**

```sql
drop schema catalogo cascade;
drop user django_catalogo;
```

E apagar o bucket `catalogo` no painel. O schema `public` e os buckets do site
não são afetados.

**Código:** último commit bom `32cc278`, branch `portfolio`.
