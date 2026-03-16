import os

templates_dir = os.path.join(os.path.dirname(__file__), 'templates', 'emails')
os.makedirs(templates_dir, exist_ok=True)

layout = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ subject }}</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f5; color: #333; margin: 0; padding: 20px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <tr>
            <td style="background-color: #0b2241; padding: 30px; text-align: center;">
                <img src="https://raw.githubusercontent.com/Philipe91/NGDSITE/main/static/img/logobranca.png" alt="NGD Logo" style="height: 45px; vertical-align: middle; margin-right: 15px;">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px; display: inline-block; vertical-align: middle;">Núcleo Gráfico Digital</h1>
            </td>
        </tr>
        <tr>
            <td style="padding: 40px 30px;">
                <!-- CONTENT_PLACEHOLDER -->
            </td>
        </tr>
        <tr>
            <td style="background-color: #f8fafc; padding: 20px; text-align: center; border-top: 1px solid #e2e8f0;">
                <p style="margin: 0; font-size: 14px; color: #64748b;">Núcleo Gráfico Digital &copy; 2026. Todos os direitos reservados.</p>
                <p style="margin: 5px 0 0 0; font-size: 14px; color: #64748b;">
                    <a href="{{ site_url }}" style="color: #3b82f6; text-decoration: none;">Acesse nosso site</a>
                </p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

created_content = """<h2 style="color: #0b2241; margin-top: 0;">Olá, {{ order.customer_name }}! 👋</h2>
<p style="font-size: 16px; line-height: 1.5; margin-bottom: 20px;">Recebemos o seu pedido <strong>#{{ order.id }}</strong> com sucesso. Agradecemos por escolher a NGD!</p>

<div style="background-color: #f1f5f9; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
    <h3 style="margin-top: 0; color: #0f172a; font-size: 16px;">Detalhes do Pedido</h3>
    <ul style="list-style: none; padding: 0; margin: 0; font-size: 15px;">
        <li style="margin-bottom: 8px;"><strong>Status:</strong> Aguardando Pagamento ⏳</li>
        <li style="margin-bottom: 8px;"><strong>Entrega:</strong> {{ order.shipping_method }}</li>
        <li><strong>Total:</strong> R$ {{ order.total|floatformat:2 }}</li>
    </ul>
</div>

<p style="font-size: 16px; line-height: 1.5;">Estamos aguardando a confirmação do pagamento para dar início à produção do seu pedido.</p>

<div style="text-align: center; margin-top: 30px;">
    <a href="{{ site_url }}/minha-conta/pedidos/{{ order.id }}/" style="background-color: #3b82f6; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; display: inline-block;">Acompanhar Pedido</a>
</div>
"""

approved_content = """<h2 style="color: #10b981; margin-top: 0;">Pagamento Aprovado! 🎉</h2>
<p style="font-size: 16px; line-height: 1.5; margin-bottom: 20px;">Olá {{ order.customer_name }}, o pagamento do seu pedido <strong>#{{ order.id }}</strong> foi confirmado.</p>

<p style="font-size: 16px; line-height: 1.5;">Se o seu pedido requer envio de artes, lembre-se de anexá-las diretamente na sua área do cliente o mais rápido possível para iniciarmos a produção!</p>

<div style="background-color: #f1f5f9; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
    <h3 style="margin-top: 0; color: #0f172a; font-size: 16px;">Próximos Passos</h3>
    <p style="margin: 0; font-size: 15px; line-height: 1.5;">O seu pedido será encaminhado para triagem e produção.</p>
</div>

<div style="text-align: center; margin-top: 30px;">
    <a href="{{ site_url }}/minha-conta/pedidos/{{ order.id }}/" style="background-color: #10b981; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; display: inline-block;">Acessar Área do Cliente</a>
</div>
"""

shipped_content = """<h2 style="color: #3b82f6; margin-top: 0;">Boas Notícias! Seu Pedido foi Liberado 🚀</h2>
<p style="font-size: 16px; line-height: 1.5; margin-bottom: 20px;">Olá {{ order.customer_name }}, o seu pedido <strong>#{{ order.id }}</strong> foi enviado ou liberado para retirada.</p>

<div style="background-color: #f1f5f9; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
    <h3 style="margin-top: 0; color: #0f172a; font-size: 16px;">Detalhes da Entrega</h3>
    <p style="margin: 0; font-size: 15px; line-height: 1.5;"><strong>Modalidade:</strong> {{ order.shipping_method }}</p>
    {% if order.shipping_method == 'Retirada na Loja' %}
    <p style="margin: 10px 0 0 0; font-size: 15px; line-height: 1.5;">Seu pedido está pronto! Por favor, entre em contato para alinhar a retirada ou venha até nossa unidade.</p>
    {% else %}
    <p style="margin: 10px 0 0 0; font-size: 15px; line-height: 1.5;">O produto já foi expedido pela transportadora e chegará no endereço cadastrado em breve.</p>
    {% endif %}
</div>

<div style="text-align: center; margin-top: 30px;">
    <a href="{{ site_url }}/minha-conta/pedidos/{{ order.id }}/" style="background-color: #3b82f6; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; display: inline-block;">Ver Detalhes do Rastreio</a>
</div>
"""

with open(os.path.join(templates_dir, 'order_created.html'), 'w', encoding='utf-8') as f:
    f.write(layout.replace('<!-- CONTENT_PLACEHOLDER -->', created_content))

with open(os.path.join(templates_dir, 'payment_approved.html'), 'w', encoding='utf-8') as f:
    f.write(layout.replace('<!-- CONTENT_PLACEHOLDER -->', approved_content))

with open(os.path.join(templates_dir, 'order_shipped.html'), 'w', encoding='utf-8') as f:
    f.write(layout.replace('<!-- CONTENT_PLACEHOLDER -->', shipped_content))

print("E-mails criados com sucesso.")
