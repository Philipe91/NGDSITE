from django.db import models

class SEOConfig(models.Model):
    site_name = models.CharField(max_length=255, default="NGD Site", verbose_name="Nome do Site")
    meta_title_default = models.CharField(max_length=255, default="NGD Site - Gráfica", verbose_name="Título Padrão (Meta Title)")
    meta_description_default = models.TextField(default="A revolução gráfica em materiais para PDV.", verbose_name="Descrição Padrão (Meta Description)")
    meta_keywords_default = models.TextField(blank=True, verbose_name="Palavras-chave (Meta Keywords)")
    og_image_default = models.ImageField(upload_to="seo/", blank=True, null=True, verbose_name="Imagem Open Graph (Padrão)")
    google_analytics_id = models.CharField(max_length=50, blank=True, verbose_name="ID Google Analytics")
    facebook_pixel_id = models.CharField(max_length=50, blank=True, verbose_name="ID Facebook Pixel")

    class Meta:
        verbose_name = "Configuração de SEO"
        verbose_name_plural = "Configurações de SEO"

    def save(self, *args, **kwargs):
        # Garante que seja um Singleton pattern (apenas 1 registro)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Configurações Globais de SEO"
