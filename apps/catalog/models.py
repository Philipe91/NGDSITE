from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Descrição", help_text="Exemplo: Categoria para placas no poliondas")
    image = models.ImageField(upload_to="categories/", blank=True, null=True, verbose_name="Imagem")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    meta_title = models.CharField(max_length=255, blank=True, verbose_name="Meta Title")
    meta_description = models.TextField(blank=True, verbose_name="Meta Description")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Categoria")
    name = models.CharField(max_length=255, verbose_name="Nome")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_description = models.TextField(blank=True, verbose_name="Descrição Curta", help_text="Exemplo: Placa de sinalização no poliondas")
    description = models.TextField(blank=True, verbose_name="Descrição", help_text="Exemplo: Descrição detalhada do material no poliondas")
    featured_image = models.ImageField(upload_to="products/featured/", blank=True, null=True, verbose_name="Imagem de Destaque")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    is_featured = models.BooleanField(default=False, verbose_name="Destaque")
    meta_title = models.CharField(max_length=255, blank=True, verbose_name="Meta Title")
    meta_description = models.TextField(blank=True, verbose_name="Meta Description")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants", verbose_name="Produto")
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU")
    size_label = models.CharField(max_length=100, verbose_name="Tamanho (Rótulo)", help_text="Ex: 40x120")
    weight_kg = models.DecimalField(max_digits=10, decimal_places=3, default=1.000, verbose_name="Peso (kg)")
    length_cm = models.DecimalField(max_digits=10, decimal_places=2, default=15.00, verbose_name="Comprimento/Prof (cm)")
    width_cm = models.DecimalField(max_length=10, max_digits=10, decimal_places=2, verbose_name="Largura (cm)")
    height_cm = models.DecimalField(max_length=10, max_digits=10, decimal_places=2, verbose_name="Altura (cm)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    template_file = models.FileField(upload_to="products/templates/", blank=True, null=True, verbose_name="Gabarito")
    manual_file = models.FileField(upload_to="products/manuals/", blank=True, null=True, verbose_name="Manual")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Variante de Produto"
        verbose_name_plural = "Variantes de Produto"

    def __str__(self):
        return f"{self.product.name} - {self.size_label}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="Produto")
    image = models.ImageField(upload_to="products/gallery/", verbose_name="Imagem")
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Texto Alternativo")
    sort_order = models.IntegerField(default=0, verbose_name="Ordem de Exibição")

    class Meta:
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens do Produto"
        ordering = ["sort_order"]

    def __str__(self):
        return f"Imagem de {self.product.name}"
