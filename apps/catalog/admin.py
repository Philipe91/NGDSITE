from django.contrib import admin
from .models import Category, Product, ProductVariant, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('name', 'short_description', 'description')
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
