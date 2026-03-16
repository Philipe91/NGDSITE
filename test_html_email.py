import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.orders.models import Order
from apps.orders.emails import send_order_created_email, send_payment_approved_email, send_order_shipped_email

# Pega o ultimo pedido feito no banco de testes ou cria um falso
order = Order.objects.last()

if not order:
    print("Criando um pedido fantasma para testar...")
    order = Order.objects.create(
        customer_name="Philipe (Teste)",
        customer_email="philipe.fernandes0101@gmail.com",
        customer_phone="11999999999",
        shipping_method="Retirada na Loja",
        total=150.00
    )
else:
    # Apenas para garantir que chegue no seu email e com seu nome na demonstração
    original_email = order.customer_email
    original_name = order.customer_name
    order.customer_email = "philipe.fernandes0101@gmail.com"
    order.customer_name = "Philipe"

print("Enviando e-mail 1: Pedido Recebido...")
send_order_created_email(order)

print("Enviando e-mail 2: Pagamento Aprovado...")
send_payment_approved_email(order)

print("Enviando e-mail 3: Pedido Enviado/Liberado...")
send_order_shipped_email(order)

# Restaura se usou um pedido real
if getattr(order, 'original_email', None):
    order.customer_email = original_email
    order.customer_name = original_name

print("\n🚀 Todos os 3 modelos de HTML foram enviados para o seu Gmail (philipe.fernandes0101@gmail.com)!")
