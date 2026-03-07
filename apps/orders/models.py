from django.db import models
from apps.catalog.models import ProductVariant

class Order(models.Model):
    STATUS_CHOICES = (
        ('aguardando_pagamento', 'Aguardando Pagamento'),
        ('pago', 'Pago'),
        ('aguardando_arte', 'Aguardando Arte'),
        ('em_producao', 'Em Produção'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    )

    customer_name = models.CharField(max_length=150, verbose_name="Nome do Cliente")
    customer_email = models.EmailField(verbose_name="E-mail")
    customer_phone = models.CharField(max_length=20, verbose_name="Telefone / WhatsApp")
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='aguardando_pagamento')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data do Pedido")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido {self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name='order_items', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.id} - {self.variant.size_label if self.variant else 'Produto Removido'}"

    def get_cost(self):
        return self.price * self.quantity
