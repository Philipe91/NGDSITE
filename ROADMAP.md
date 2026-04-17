# ROADMAP DO PROJETO - E-COMMERCE NGD

Este documento registra o nosso estado atual de desenvolvimento e os próximos passos para o Go-Live. 
Ele foi gerado no dia 09/04/2026 para mapear as funcionalidades prontas e a reta final.

---

## 📍 Onde Estamos (Fases 1 a 16 finalizadas)

**1. Estrutura e Catálogo (Fases 1-10)**
- Loja funcional com produtos, slugs amigáveis para SEO e categorias.
- **Configurador de Produto Dinâmico:** Preço muda automaticamente via JavaScript dependendo das variantes escolhidas (Material, Tamanho, Acabamento).
- Carrinho funcional com persistência e design premium.

**2. Pagamento (Fase 11)**
- Integração completa com o **Mercado Pago**.
- Pagamentos via **Cartão de Crédito** transparente e **PIX** (com baixa automática de segurança por Webhook).

**3. Fretes e Logística (Fase 12 e 16)**
- Integração da API de busca de CEP e cálculo dinâmico de frete integrado ao **Melhor Envio** / Correios.
- Opção configurável de **Retirada na Loja**.

**4. Portal do Cliente VIP (Fase 13)**
- Dashboard do cliente (Histórico de Pedidos, Status Atual).
- **Upload de Arte Pós-Pagamento:** O cliente não precisa mandar artes por WhatsApp, ele anexa direto no pedido depois de confirmada a compra.

**5. Sistema de Comunicação Automatizada (Fase 14)**
- E-mails transacionais utilizando o Gmail SMTP configurado.
- Disparo de aviso "Novo Pedido", "Pagamento Confirmado", "Pedido Liberado/Enviado".

**6. Painel Interno de Comando e Produção (Fase 15)**
- O "Backend Administrativo" onde a equipe gerencia todo o estoque.
- Aprovação/Rejeição das Artes enviadas pelos clientes.
- Fluxo de Kanban Kanban (Aguardando > Em Produção > Enviado).
- Geração e impressão da **Ordem de Serviço (O.S.)** direto do painel para o departamento braçal.

**7. Premium UI/UX Upgrade (Recente)**
- Efeito vidro (glassmorphism), dark elements, refino de tipografia e sombras completas.
- Dashboard premium e adequações em layout Mobile (Responsividade).

---

## 🚀 O Que Falta / Próximos Passos Pós-Teste Restante (Go-Live)

1. **Testes do "Mundo Real":** Adicionar as variantes de produtos (Rollup, Faixas, Placas) **corretas e manuais** através do painel Admin. Gerar imagens com Mockups reais. *(Etapa que está sendo feita pelo Head do projeto)*.
2. **Atualização Institucional:** Alterar "Políticas de Troca e Privacidade", adicionando informações e CNPJ oficial aos termos para estar 100% de acordo com as exigências.
3. **Migração do Banco de Dados:** Mudar de banco local "SQLite" para PostgreSQL robusto (necessário quando as visitas bombarem na loja pra aguentar a carga).
4. **Deploy e Servidor Online:** Mover os dados deste computador/ambiente local para uma nuvem online (Hostinger, AWS, Heroku, etc.).
5. **Apontamento do Domínio Final e SSL:** Anexar o `.com.br` novo com certificado de Segurança (Cadeado Verde HTTPS). *Sem o Cadeado HTTPS o Mercado Pago de Produção não libera compras reais.*
6. **Abertura:** Lançamento público da plataforma para clientes B2C/B2B com compras abertas.
