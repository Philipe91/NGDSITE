import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.pages.models import Page

# ─── POLÍTICA DE PRIVACIDADE ──────────────────────────────────────────────────
privacidade_html = """
<div class="max-w-3xl mx-auto py-12 px-4 text-gray-700">

  <p class="text-sm text-gray-400 mb-8">Última atualização: 13 de março de 2026</p>

  <p class="mb-6 leading-relaxed">
    A <strong>NGD – Núcleo Gráfico Digital Ltda.</strong>, inscrita no CNPJ <strong>12.345.678/0001-00</strong>,
    com sede em Brasília/DF, respeita a sua privacidade e está comprometida com a proteção dos seus dados
    pessoais, em conformidade com a <strong>Lei Geral de Proteção de Dados (LGPD – Lei nº 13.709/2018)</strong>
    e o <strong>Código de Defesa do Consumidor (Lei nº 8.078/1990)</strong>.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">1. Quais dados coletamos</h2>
  <ul class="list-disc pl-6 space-y-2 mb-6">
    <li><strong>Dados de identificação:</strong> nome, e-mail, CPF/CNPJ, telefone.</li>
    <li><strong>Dados de entrega:</strong> endereço completo e CEP.</li>
    <li><strong>Dados de pagamento:</strong> processados exclusivamente pelo Mercado Pago (não armazenamos dados de cartão).</li>
    <li><strong>Arquivos de arte:</strong> arquivos enviados para produção gráfica.</li>
    <li><strong>Dados de navegação:</strong> IP, cookies técnicos e de desempenho, páginas acessadas.</li>
  </ul>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">2. Como usamos seus dados</h2>
  <ul class="list-disc pl-6 space-y-2 mb-6">
    <li>Processar e entregar seus pedidos.</li>
    <li>Enviar confirmações de pedido e atualizações de entrega.</li>
    <li>Cumprir obrigações fiscais e legais.</li>
    <li>Melhorar nossos produtos e serviços.</li>
    <li>Enviar comunicações de marketing (somente com seu consentimento, cancelável a qualquer momento).</li>
  </ul>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">3. Base legal para o tratamento</h2>
  <ul class="list-disc pl-6 space-y-2 mb-6">
    <li><strong>Execução de contrato</strong> (art. 7º, V, LGPD): para processar seu pedido.</li>
    <li><strong>Obrigação legal</strong> (art. 7º, II, LGPD): para emissão de notas fiscais e registros contábeis.</li>
    <li><strong>Legítimo interesse</strong> (art. 7º, IX, LGPD): para segurança e melhoria dos serviços.</li>
    <li><strong>Consentimento</strong> (art. 7º, I, LGPD): para comunicações de marketing.</li>
  </ul>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">4. Com quem compartilhamos</h2>
  <ul class="list-disc pl-6 space-y-2 mb-6">
    <li><strong>Mercado Pago:</strong> processamento de pagamentos.</li>
    <li><strong>Transportadoras:</strong> para entrega de produtos.</li>
    <li><strong>Autoridades públicas:</strong> quando exigido por lei.</li>
  </ul>
  <p class="mb-6">Não vendemos, alugamos nem compartilhamos seus dados com terceiros para fins comerciais.</p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">5. Por quanto tempo guardamos seus dados</h2>
  <p class="mb-6">
    Dados de pedido e fiscais são mantidos por <strong>5 anos</strong> conforme exigência legal (legislação tributária).
    Arquivos de arte são mantidos por <strong>90 dias</strong> após conclusão do pedido e então eliminados.
    Dados de marketing são eliminados imediatamente após cancelamento do consentimento.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">6. Seus direitos (LGPD)</h2>
  <p class="mb-4">Em conformidade com o art. 18 da LGPD, você tem direito a:</p>
  <ul class="list-disc pl-6 space-y-2 mb-6">
    <li>Confirmar a existência de tratamento dos seus dados.</li>
    <li>Acessar seus dados pessoais.</li>
    <li>Corrigir dados incompletos, inexatos ou desatualizados.</li>
    <li>Solicitar a anonimização, bloqueio ou eliminação dos seus dados.</li>
    <li>Revogar o consentimento a qualquer momento.</li>
    <li>Apresentar reclamação à <strong>ANPD (Autoridade Nacional de Proteção de Dados)</strong>.</li>
  </ul>
  <p class="mb-6">Para exercer seus direitos, entre em contato pelo e-mail: <a href="mailto:ngd@nucleografico.com.br" class="text-primary hover:underline">ngd@nucleografico.com.br</a></p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">7. Cookies</h2>
  <p class="mb-6">
    Utilizamos cookies técnicos (necessários para o funcionamento do site) e cookies de desempenho (para melhorar a experiência).
    Você pode gerenciar suas preferências de cookies pelo banner exibido no primeiro acesso ao site.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">8. Segurança</h2>
  <p class="mb-6">
    Adotamos medidas técnicas e organizacionais para proteger seus dados contra acesso não autorizado, perda ou alteração,
    incluindo criptografia SSL/TLS, controle de acesso e backups regulares.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">9. Contato e DPO</h2>
  <p class="mb-2"><strong>NGD – Núcleo Gráfico Digital Ltda.</strong></p>
  <p class="mb-2">CNPJ: 12.345.678/0001-00</p>
  <p class="mb-2">E-mail: <a href="mailto:ngd@nucleografico.com.br" class="text-primary hover:underline">ngd@nucleografico.com.br</a></p>
  <p class="mb-2">Telefone: (61) 99649-8102</p>
  <p class="mb-6">Horário de atendimento: Segunda a Sexta, das 8h às 18h.</p>

</div>
"""

# ─── TERMOS DE USO ────────────────────────────────────────────────────────────
termos_html = """
<div class="max-w-3xl mx-auto py-12 px-4 text-gray-700">

  <p class="text-sm text-gray-400 mb-8">Última atualização: 13 de março de 2026</p>

  <p class="mb-6 leading-relaxed">
    Bem-vindo ao site da <strong>NGD – Núcleo Gráfico Digital Ltda.</strong> Ao acessar e utilizar este site,
    você concorda com os presentes Termos de Uso. Caso não concorde, por favor, não utilize nossos serviços.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">1. Sobre a empresa</h2>
  <p class="mb-6">
    NGD – Núcleo Gráfico Digital Ltda., CNPJ <strong>12.345.678/0001-00</strong>, com sede em Brasília/DF,
    é uma indústria especializada em materiais gráficos para PDV (Ponto de Venda), atuando há mais de 18 anos
    no mercado de comunicação visual.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">2. Produtos e pedidos</h2>
  <ul class="list-disc pl-6 space-y-2 mb-6">
    <li>Os preços exibidos são em Reais (R$) e incluem impostos aplicáveis, salvo indicação contrária.</li>
    <li>A confirmação do pedido está condicionada à aprovação do pagamento e à disponibilidade de produção.</li>
    <li>O prazo de produção começa a contar após a aprovação do arquivo de arte pela equipe técnica.</li>
    <li>Pedidos com arquivos fora das especificações técnicas exigem reenvio, o que pode alterar o prazo.</li>
  </ul>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">3. Pagamento</h2>
  <p class="mb-6">
    Aceitamos pagamento via <strong>Pix</strong> e <strong>cartão de crédito</strong>, processados pelo Mercado Pago.
    O pedido é confirmado somente após a confirmação do pagamento pela plataforma de pagamento.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">4. Frete e entrega</h2>
  <ul class="list-disc pl-6 space-y-2 mb-6">
    <li>O prazo de entrega é estimado e pode variar por fatores externos (Correios, transportadora, greves).</li>
    <li>O cliente será informado sobre o status do pedido por e-mail.</li>
    <li>A NGD não se responsabiliza por atrasos causados por informações de endereço incorretas fornecidas pelo cliente.</li>
  </ul>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">5. Direito de arrependimento (CDC)</h2>
  <p class="mb-6">
    Conforme o <strong>art. 49 do Código de Defesa do Consumidor</strong>, o cliente tem direito de desistir
    de compras realizadas pela internet em até <strong>7 dias corridos</strong> após o recebimento do produto.
    Produtos personalizados e produzidos sob encomenda (com arquivo de arte aprovado e produção iniciada)
    estão isentos deste direito, salvo defeito de fabricação comprovado.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">6. Upload de arquivos de arte</h2>
  <ul class="list-disc pl-6 space-y-2 mb-6">
    <li>O cliente é responsável por enviar arquivos dentro das especificações técnicas indicadas no gabarito.</li>
    <li>A NGD realizará uma revisão técnica básica (resolução, sangria, modo de cor).</li>
    <li>Arquivos aprovados sem observações passam diretamente para produção.</li>
    <li>A NGD não se responsabiliza por erros de conteúdo (texto, imagem, cores) em arquivos aprovados pelo cliente.</li>
  </ul>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">7. Propriedade intelectual</h2>
  <p class="mb-6">
    Todo o conteúdo deste site (textos, imagens, logotipos, layouts) é de propriedade da NGD ou de seus licenciantes.
    É proibida a reprodução, distribuição ou uso comercial sem autorização prévia por escrito.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">8. Limitação de responsabilidade</h2>
  <p class="mb-6">
    A NGD não se responsabiliza por danos indiretos, lucros cessantes ou prejuízos decorrentes do uso inadequado
    dos produtos ou de interrupções do serviço por fatores fora do controle da empresa (caso fortuito ou força maior).
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">9. Foro e lei aplicável</h2>
  <p class="mb-6">
    Estes termos são regidos pela legislação brasileira. Eventuais conflitos serão resolvidos no
    <strong>Foro da Comarca de Brasília/DF</strong>, com renúncia a qualquer outro, por mais privilegiado que seja.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">10. Contato</h2>
  <p class="mb-2">E-mail: <a href="mailto:ngd@nucleografico.com.br" class="text-primary hover:underline">ngd@nucleografico.com.br</a></p>
  <p class="mb-2">Telefone: (61) 99649-8102</p>
  <p class="mb-6">Horário: Segunda a Sexta, das 8h às 18h.</p>

</div>
"""

# ─── POLITICA DE COOKIES ──────────────────────────────────────────────────────
cookies_html = """
<div class="max-w-3xl mx-auto py-12 px-4 text-gray-700">

  <p class="text-sm text-gray-400 mb-8">Última atualização: 13 de março de 2026</p>

  <p class="mb-6 leading-relaxed">
    Este site utiliza <strong>cookies</strong> para garantir o funcionamento correto, melhorar a sua experiência e
    cumprir obrigações legais. Esta política explica o que são cookies, quais utilizamos e como você pode controlá-los.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">O que são cookies?</h2>
  <p class="mb-6">
    Cookies são pequenos arquivos de texto armazenados no seu navegador quando você visita um site.
    Eles permitem que o site lembre suas preferências e sessão de navegação.
  </p>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">Cookies que utilizamos</h2>
  <div class="overflow-x-auto mb-8">
    <table class="w-full text-sm border-collapse">
      <thead>
        <tr class="bg-gray-100">
          <th class="text-left p-3 border border-gray-200">Nome</th>
          <th class="text-left p-3 border border-gray-200">Tipo</th>
          <th class="text-left p-3 border border-gray-200">Finalidade</th>
          <th class="text-left p-3 border border-gray-200">Duração</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="p-3 border border-gray-200">sessionid</td>
          <td class="p-3 border border-gray-200">Necessário</td>
          <td class="p-3 border border-gray-200">Manter a sessão do usuário logado</td>
          <td class="p-3 border border-gray-200">Sessão</td>
        </tr>
        <tr class="bg-gray-50">
          <td class="p-3 border border-gray-200">csrftoken</td>
          <td class="p-3 border border-gray-200">Necessário</td>
          <td class="p-3 border border-gray-200">Proteção contra ataques CSRF</td>
          <td class="p-3 border border-gray-200">1 ano</td>
        </tr>
        <tr>
          <td class="p-3 border border-gray-200">cart</td>
          <td class="p-3 border border-gray-200">Necessário</td>
          <td class="p-3 border border-gray-200">Manter itens no carrinho de compras</td>
          <td class="p-3 border border-gray-200">Sessão</td>
        </tr>
        <tr class="bg-gray-50">
          <td class="p-3 border border-gray-200">ngd_cookie_consent</td>
          <td class="p-3 border border-gray-200">Preferência</td>
          <td class="p-3 border border-gray-200">Guardar sua escolha sobre cookies</td>
          <td class="p-3 border border-gray-200">1 ano</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h2 class="text-xl font-bold text-gray-900 mt-10 mb-4 border-b pb-2">Como gerenciar cookies</h2>
  <p class="mb-4">
    Você pode configurar seu navegador para recusar todos ou alguns cookies.
    Note que desabilitar cookies necessários pode impedir o funcionamento do carrinho e do login.
  </p>
  <ul class="list-disc pl-6 space-y-2 mb-6">
    <li><a href="https://support.google.com/chrome/answer/95647" target="_blank" class="text-primary hover:underline">Google Chrome</a></li>
    <li><a href="https://support.mozilla.org/pt-BR/kb/cookies-informacoes-que-os-sites-armazenam-no-seu-c" target="_blank" class="text-primary hover:underline">Mozilla Firefox</a></li>
    <li><a href="https://support.apple.com/pt-br/guide/safari/sfri11471/mac" target="_blank" class="text-primary hover:underline">Safari</a></li>
    <li><a href="https://support.microsoft.com/pt-br/microsoft-edge/excluir-cookies-no-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09" target="_blank" class="text-primary hover:underline">Microsoft Edge</a></li>
  </ul>

  <p class="text-sm text-gray-500">
    Para mais informações sobre cookies em geral, acesse <a href="https://www.allaboutcookies.org" target="_blank" class="text-primary hover:underline">www.allaboutcookies.org</a>.
  </p>
</div>
"""

pages = [
    {
        "slug": "privacidade",
        "title": "Política de Privacidade",
        "content": privacidade_html,
    },
    {
        "slug": "termos-e-condicoes",
        "title": "Termos de Uso",
        "content": termos_html,
    },
    {
        "slug": "politica-de-cookies",
        "title": "Política de Cookies",
        "content": cookies_html,
    },
]

for p in pages:
    obj, created = Page.objects.get_or_create(slug=p["slug"])
    obj.title = p["title"]
    obj.content = p["content"]
    obj.is_published = True
    obj.save()
    status = "criada" if created else "atualizada"
    print(f"  {p['title']}: {status}")

print("\nPronto! Todas as páginas legais foram salvas.")
