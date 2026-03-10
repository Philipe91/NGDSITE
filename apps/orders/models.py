from django.db import models
from django.utils import timezone
from apps.catalog.models import ProductVariant


def order_item_art_upload_path(instance, filename):
    created_at = instance.order.created_at if instance.order_id and instance.order.created_at else timezone.now()
    return f"uploads/artes/{created_at:%Y/%m/%d}/{filename}"

class Order(models.Model):
    SHIPPING_METHOD_CHOICES = (
        ('retirada', 'Retirada na Loja'),
        ('frete_fixo', 'Frete Fixo'),
    )

    STATUS_CHOICES = (
        ('aguardando_pagamento', 'Aguardando Pagamento'),
        ('pago', 'Pago'),
        ('aguardando_arte', 'Aguardando Arte'),
        ('arte_recebida', 'Arte Recebida'),
        ('em_producao', 'Em Produção'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    )

    customer_name = models.CharField(max_length=150, verbose_name="Nome do Cliente")
    customer_email = models.EmailField(verbose_name="E-mail")
    customer_phone = models.CharField(max_length=20, verbose_name="Telefone / WhatsApp")

    # Frete
    shipping_method = models.CharField(
        max_length=20, choices=SHIPPING_METHOD_CHOICES,
        default='retirada', verbose_name="Método de Entrega"
    )
    shipping_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Custo do Frete"
    )
    shipping_cep = models.CharField(max_length=9, blank=True, verbose_name="CEP de Entrega")
    shipping_address = models.TextField(blank=True, verbose_name="Endereço de Entrega")

    # Pagamento
    mp_payment_id = models.CharField(max_length=100, blank=True, verbose_name="ID Pagamento MP")
    mp_preference_id = models.CharField(max_length=100, blank=True, verbose_name="ID Preferência MP")

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
    ART_STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    )

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name='order_items', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")
    art_file = models.FileField(upload_to=order_item_art_upload_path, blank=True, null=True, verbose_name="Arquivo da Arte")
    art_status = models.CharField(max_length=20, choices=ART_STATUS_CHOICES, default='pendente', verbose_name="Status da Arte")

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.id} - {self.variant.size_label if self.variant else 'Produto Removido'}"

    def get_cost(self):
        return self.price * self.quantity

    @property
    def has_art_file(self):
        return bool(self.art_file)
