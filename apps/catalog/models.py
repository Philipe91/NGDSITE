from django.db import models
from django.utils.text import slugify
from django.urls import reverse

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

    def get_absolute_url(self):
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})

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

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

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


class MegaMenuTotensCard(models.Model):
    """Cards do megamenu 'Totens PDV'. Cada linha vira um card no header.
    Permite ao admin editar imagem, título, badge, ordem e link sem mexer em template."""

    BADGE_NONE = ""
    BADGE_NEW = "novo"
    BADGE_BEST = "mais_vendido"
    BADGE_SOON = "em_breve"
    BADGE_HOT = "destaque"
    BADGE_CHOICES = [
        (BADGE_NONE, "— sem badge —"),
        (BADGE_NEW, "Novo"),
        (BADGE_BEST, "Mais vendido"),
        (BADGE_SOON, "Em breve"),
        (BADGE_HOT, "Destaque"),
    ]

    title = models.CharField(
        max_length=80,
        verbose_name="Título do card",
        help_text="Ex: Totem Triangular",
    )
    image = models.ImageField(
        upload_to="megamenu/totens/",
        blank=True,
        null=True,
        verbose_name="Imagem do card",
        help_text="Recomendado: PNG transparente, ~600x800px",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="megamenu_cards",
        verbose_name="Produto vinculado",
        help_text="Se preenchido, o card linka para a página do produto e usa o preço da 1ª variante.",
    )
    custom_url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="URL customizada",
        help_text="Opcional. Se preenchido, sobrescreve o link do produto.",
    )
    badge = models.CharField(
        max_length=20,
        choices=BADGE_CHOICES,
        blank=True,
        default=BADGE_NONE,
        verbose_name="Selo / Badge",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Card Megamenu Totens PDV"
        verbose_name_plural = "Megamenu Totens PDV"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def link(self):
        if self.custom_url:
            return self.custom_url
        if self.product_id:
            return self.product.get_absolute_url()
        return "#"

    @property
    def starting_price(self):
        if not self.product_id:
            return None
        v = self.product.variants.filter(is_active=True).order_by("price").first()
        return v.price if v else None
