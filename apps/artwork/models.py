from django.db import models
from apps.orders.models import Order


def artwork_upload_path(instance, filename):
    return f'artworks/pedido_{instance.order.id}/{filename}'


class ArtworkFile(models.Model):
    order = models.ForeignKey(Order, related_name='artworks', on_delete=models.CASCADE, verbose_name="Pedido")
    file = models.FileField(upload_to=artwork_upload_path, verbose_name="Arquivo de Arte")
    original_name = models.CharField(max_length=255, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado em")
    notes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Arte do Cliente"
        verbose_name_plural = "Artes dos Clientes"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Arte Pedido #{self.order.id} — {self.original_name}"

    def save(self, *args, **kwargs):
        if not self.original_name and self.file:
            self.original_name = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)
