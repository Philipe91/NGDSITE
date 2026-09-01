# Tarefa: publicar a loja no Cloud Run

Leia inteiro antes de começar. Trabalhe sempre em `C:\projetos\NGDPORTFOLIO`.
O Python é `./venv/Scripts/python.exe`.

---

## Contexto

A NGD tem **dois projetos diferentes**. Confundir os dois derruba um site que fatura:

| | Onde fica | O que é |
|---|---|---|
| **Site institucional** | `C:\projetos\nucleografico\Github` | **NO AR** em nucleografico.com.br. React + Vite no Firebase Hosting. 38 páginas indexadas. |
| **Loja** | `C:\projetos\NGDPORTFOLIO` | Django. **JÁ ESTÁ NO AR** em nucleografico.com.br/loja, servida pelo Cloud Run. É o que você vai atualizar. |

O Firebase encaminha `/loja/**` para o serviço `ngd-loja` no Cloud Run, região
`us-west1`. Essa configuração já está publicada e commitada. **Você não precisa
tocar no Firebase.**

O que vai ao ar são correções de SEO e de peso das páginas, já commitadas e
verificadas. Commit `00bbde0`, branch `portfolio`.

---

## Regras que não podem ser quebradas

1. **Não altere nada em `C:\projetos\nucleografico`.** Leitura é permitida;
   escrita não. Existe lá um `public/sitemap.xml` modificado e não commitado
   que é trabalho do dono — não encoste.
2. **Não rode `firebase deploy`.** Esta tarefa é só Cloud Run. O menu "Loja" do
   site institucional é outro assunto, com aprovação à parte.
3. **Não rode migrations pelo pooler** (porta 6543). Se precisar, use a conexão
   direta na 5432.
4. **Não apague nada do bucket `catalogo` do Supabase.** Os PNG originais estão
   lá de propósito: são a reversão da otimização de imagens.

Se algo não estiver claro, **pergunte antes de agir**.

---

## Antes de começar

Confirme o commit e a árvore limpa:

    git -C C:\projetos\NGDPORTFOLIO log --oneline -1     # deve ser 00bbde0
    git -C C:\projetos\NGDPORTFOLIO status --short       # deve estar vazio

Confirme que a loja está no ar agora, para saber o estado inicial:

    curl -s -o /dev/null -w "%{http_code}\n" https://nucleografico.com.br/loja/

---

## Passo 1 — Deploy

    gcloud run deploy ngd-loja --source . --region us-west1

O `Dockerfile` e o `.dockerignore` já estão prontos. O build roda
`collectstatic` sozinho.

**Não altere as variáveis de ambiente do serviço.** Elas já estão configuradas
no Cloud Run e o contêiner as lê de lá — o arquivo `.env.production` é só
referência local e fica fora da imagem de propósito.

Se o deploy falhar com `SITE_URL não configurado para produção`, é porque a
variável `SITE_URL` não existe no serviço. Nesse caso **pare e avise**: o valor
correto é `https://nucleografico.com.br/loja`, mas quem define isso é o dono.

Ao final, o Cloud Run devolve uma URL `...run.app`. Teste por ela primeiro.

---

## Passo 2 — Apontar o banco de produção para as imagens WebP

63 imagens foram convertidas de PNG para WebP (67,7 MB para 5,4 MB). Os
arquivos `.webp` **já estão no bucket**, mas o banco de produção ainda aponta
para os PNG. Este comando só troca o ponteiro, não reenvia nada.

Ele precisa das variáveis do `.env.production`. Como o Django só carrega
`.env`, o caminho mais simples é copiar `.env.production` sobre `.env` —
**guardando antes uma cópia do `.env` original e devolvendo depois.**

    python manage.py otimizar_imagens --simular    # confira a lista primeiro
    python manage.py otimizar_imagens

Esperado: 63 imagens, cada uma apenas trocando o ponteiro, sem reenvio. Ele
grava um mapa em `backups/` para reversão.

---

## Passo 3 — Conferir

    curl -s https://nucleografico.com.br/loja/produto/banner-rollup/ | grep -oE 'rel="canonical" href="[^"]+"'

Precisa sair **`https://nucleografico.com.br/loja/produto/banner-rollup/`**.

Três coisas que NÃO podem aparecer em nenhuma página:

- `run.app` no canonical, no og:url ou no sitemap — era o bug principal desta leva
- `/loja/loja/` — caminho duplicado
- `https://...https://...` — URL dupla nas imagens

Confira também:

    curl -s https://nucleografico.com.br/loja/sitemap.xml | grep -c "<loc>"   # 25
    curl -s https://nucleografico.com.br/loja/ | grep -c "\.webp"             # maior que 0

E abra no navegador: home, três páginas de produto e Quem Somos. As imagens
devem carregar visivelmente mais rápido.

---

## Se der errado

**Voltar o deploy:** o Cloud Run mantém as revisões anteriores.

    gcloud run revisions list --service ngd-loja --region us-west1
    gcloud run services update-traffic ngd-loja --region us-west1 --to-revisions <REVISAO_ANTERIOR>=100

Pelo console dá no mesmo: Cloud Run > ngd-loja > Revisões > mandar 100% do
tráfego para a revisão anterior. Volta em segundos.

**Voltar as imagens:** os PNG continuam no bucket.

    python manage.py otimizar_imagens --desfazer backups/otimizacao-imagens-<data>.json

**Voltar o código:** `git reset --hard 00bbde0`.

---

## O que NÃO faz parte desta tarefa

- Deploy do site institucional (`firebase deploy`), que inclui o item "Loja" no
  menu e aguarda aprovação do dono.
- Rotação de credenciais. O `SECRET_KEY` de produção precisa ser trocado, mas é
  decisão e ação do dono.
- Criar o superusuário de produção.

Pare quando o passo 3 estiver conferido e relate o que encontrou.
