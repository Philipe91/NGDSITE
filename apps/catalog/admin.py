from django import forms
from django.contrib import admin
from django.db import models
from image_uploader_widget.widgets import ImageUploaderWidget
from .models import Category, Product, ProductVariant, ProductImage, MegaMenuTotensCard


class ProductImageInlineForm(forms.ModelForm):
    """Linhas novas sem imagem (geradas pelo widget JS quando o usuário cancela
    crop/seleção ou após re-render por erro de outro campo) são silenciosamente
    descartadas em vez de barrar o save com 'image obrigatório'."""

    class Meta:
        model = ProductImage
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.empty_permitted = True

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'image', 'is_active')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )

class ProductVariantInline(admin.StackedInline):
    model = ProductVariant
    extra = 0
    fieldsets = (
        ('Informações Principais', {
            'fields': (('sku', 'size_label'), ('price', 'is_active'))
        }),
        ('Logística e Dimensões', {
            'fields': (('weight_kg', 'length_cm', 'width_cm', 'height_cm'),)
        }),
        ('Arquivos Anexos (Opcional)', {
            'fields': (('template_file', 'manual_file'),),
            'classes': ('collapse',)
        }),
    )

from image_uploader_widget.admin import OrderedImageUploaderInline

class ProductImageInline(OrderedImageUploaderInline):
    model = ProductImage
    form = ProductImageInlineForm
    extra = 0
    order_field = "sort_order"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.13/cropper.min.js',
            'js/admin_cropper.js',
        )
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.13/cropper.min.css',)
        }
    list_display = ('name', 'category', 'is_active', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('name', 'short_description', 'description')
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'short_description', 'description', 'featured_image', 'is_active', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )
    inlines = [ProductVariantInline, ProductImageInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'size_label', 'price', 'is_active')
    list_filter = ('is_active', 'product')
    search_fields = ('sku', 'product__name', 'size_label')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'sort_order')
    list_filter = ('product',)
    search_fields = ('product__name',)


@admin.register(MegaMenuTotensCard)
class MegaMenuTotensCardAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'product', 'badge', 'is_active', 'image_thumb')
    list_display_links = ('title',)
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'badge')
    search_fields = ('title', 'product__name')
    autocomplete_fields = ('product',)
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }
    fieldsets = (
        ('Conteúdo do card', {
            'fields': ('title', 'image', 'badge')
        }),
        ('Link do card', {
            'fields': ('product', 'custom_url'),
            'description': 'Vincule a um produto (recomendado) OU defina uma URL customizada. Se ambos estiverem preenchidos, a URL customizada vence.',
        }),
        ('Exibição', {
            'fields': ('order', 'is_active')
        }),
    )

    def image_thumb(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html(
                '<img src="{}" style="height:48px;width:auto;border-radius:6px;border:1px solid #e5e7eb;" />',
                obj.image.url,
            )
        return "—"
    image_thumb.short_description = "Imagem"
