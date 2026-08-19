# 🎬 Como mostrar o site pro chefe aprovar

O site é um sistema **Django** (Python + banco de dados). Ele **não roda no Netlify**
(que é só pra sites estáticos). Para uma apresentação rápida de aprovação, o caminho
ideal é o **link público temporário** via Cloudflare Tunnel — mostra o site 100% real,
com todas as imagens e funções, sem precisar contratar nada.

---

## ✅ Passo a passo (leva 1 minuto)

1. Dê **duplo clique** no arquivo **`APRESENTACAO_TUNEL.bat`** (na pasta do projeto).
2. Espere alguns segundos. Vai aparecer uma URL parecida com:

   ```
   https://algo-aleatorio.trycloudflare.com
   ```

3. **Copie essa URL** e envie pro seu chefe (WhatsApp, e-mail, etc).
4. Ele abre o link no celular ou computador, de qualquer lugar, e vê o site funcionando.

> A janela preta (terminal) precisa **ficar aberta** enquanto o chefe estiver acessando.
> Quando fechar a janela, o link para de funcionar.

---

## ⚠️ O que avisar pro chefe (é uma PRÉVIA)

Deixe claro que é uma **demonstração para aprovação**, ainda não é o site final no ar:

- O link é **temporário** (muda toda vez que você abre o `.bat`).
- Pode ficar um pouco mais lento (passa pelo seu computador).
- O **pagamento está em modo teste** (não cobra de verdade ainda).
- O site **ainda não tem domínio próprio** nem HTTPS oficial.

Tudo isso é resolvido no deploy real (próximo passo, após a aprovação).

---

## 📋 O que já está pronto pra mostrar

- Catálogo completo (9 produtos com fotos, preços, descrições e FAQ)
- Cadastro profissional (Pessoa Física / Jurídica com CPF/CNPJ pra nota fiscal)
- Carrinho e checkout
- Painel do cliente (acompanhar pedidos)
- Painel administrativo com Kanban de produção
- Widget de WhatsApp, páginas institucionais (privacidade, termos, etc)

---

## 🚀 Depois da aprovação — o que falta pro site no ar

(Já está tudo planejado; me chame que eu conduzo cada passo)

1. **Comprar domínio** (ex: nucleografico.com.br — ~R$ 40/ano no Registro.br)
2. **Contratar hospedagem** que rode Django:
   - **Render.com** ou **Railway** (mais simples, a partir de ~US$ 7/mês)
   - ou **VPS** (Hostinger / DigitalOcean / Hetzner — ~R$ 30–80/mês, mais controle)
3. **Ativar HTTPS** (cadeado de segurança — grátis via Let's Encrypt/Cloudflare)
4. **Rotacionar as credenciais** e **ativar o pagamento real** (Mercado Pago produção)
5. **Cadastrar no Google Search Console** (pra aparecer nas buscas)

A stack de produção (Gunicorn, Nginx, Procfile) já está pronta no projeto —
o site sobe rápido assim que o domínio e a hospedagem estiverem definidos.
