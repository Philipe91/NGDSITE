from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['variant']
    extra = 0
    fields = ['variant', 'quantity', 'price', 'art_status', 'art_download']
    readonly_fields = ['art_download']

    def art_download(self, obj):
        if obj.art_file:
            return format_html('<a href="{}" target="_blank">Baixar arte</a>', obj.art_file.url)
        return "Sem arquivo"

    art_download.short_description = "Arquivo da Arte"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'variant', 'quantity', 'price', 'art_status', 'art_download']
    list_filter = ['art_status', 'order__status']
    search_fields = ['order__customer_name', 'order__customer_email', 'variant__product__name', 'variant__sku']
    raw_id_fields = ['order', 'variant']
    readonly_fields = ['art_download']
    fields = ['order', 'variant', 'quantity', 'price', 'art_file', 'art_download', 'art_status']

    def art_download(self, obj):
        if obj.art_file:
            return format_html('<a href="{}" target="_blank">Baixar arte</a>', obj.art_file.url)
        return "Sem arquivo"

    art_download.short_description = "Arquivo da Arte"
