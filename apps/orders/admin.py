from django.contrib import admin
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.urls import reverse
from .models import Order, OrderItem, PainelDeProducao, ShippingConfig
from .emails import send_order_shipped_email


# ---------------------------------------------------------------------------
# Inline de itens
# ---------------------------------------------------------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['variant']
    extra = 0
    fields = ['variant', 'quantity', 'price', 'art_status', 'art_download']
    readonly_fields = ['art_download']

    def art_download(self, obj):
        if obj.art_file:
            return format_html(
                '<a href="{}" target="_blank" style="color:#2563eb;font-weight:600;">Baixar arte</a>',
                obj.art_file.url
            )
        return "Sem arquivo"
    art_download.short_description = "Arquivo da Arte"


# ---------------------------------------------------------------------------
# Ícones SVG por status (Heroicons stroke-2, 12px)
# ---------------------------------------------------------------------------
_SVG = 'width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24" style="vertical-align:middle;margin-right:5px;"'

STATUS_CFG = {
    # status:  (bg, text-color, svg-path)
    'aguardando_pagamento': ('#f1f5f9', '#475569',
        f'<svg {_SVG}><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>'),
    'pago': ('#dbeafe', '#1e40af',
        f'<svg {_SVG}><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>'),
    'aguardando_arte': ('#fff7ed', '#9a3412',
        f'<svg {_SVG}><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>'),
    'arte_recebida': ('#fef9c3', '#854d0e',
        f'<svg {_SVG}><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>'),
    'em_producao': ('#ede9fe', '#4c1d95',
        f'<svg {_SVG}><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93A10 10 0 003 12"/><path d="M4.93 19.07A10 10 0 0021 12"/></svg>'),
    'enviado': ('#dcfce7', '#14532d',
        f'<svg {_SVG}><path d="M5 12h14M12 5l7 7-7 7"/></svg>'),
    'entregue': ('#d1fae5', '#064e3b',
        f'<svg {_SVG}><polyline points="20 6 9 17 4 12"/></svg>'),
    'cancelado': ('#fee2e2', '#7f1d1d',
        f'<svg {_SVG}><circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6M9 9l6 6"/></svg>'),
}


# ---------------------------------------------------------------------------
# OrderAdmin
# ---------------------------------------------------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'review_badge', 'customer_name', 'customer_email',
                    'colored_status', 'total', 'tracking_code', 'created_at']
    list_filter   = ['status', 'reviewed', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    inlines       = [OrderItemInline]
    actions       = ['marcar_revisado', 'desmarcar_revisado', 'enviar_para_kanban', 'print_os']
    readonly_fields = ['customer_panel', 'created_at', 'updated_at',
                       'mp_payment_id', 'mp_preference_id', 'subtotal', 'total']

    fieldsets = (
        ('👤 Ficha do Cliente', {
            'fields': ('customer_panel',),
        }),
        ('Dados de contato', {
            'fields': (('customer_name',), ('customer_email', 'customer_phone')),
        }),
        ('Entrega', {
            'fields': ('shipping_method', 'shipping_cep', 'shipping_address', 'tracking_code'),
        }),
        ('Pagamento & valores', {
            'fields': (('subtotal', 'shipping_cost', 'total'),
                       ('mp_payment_id', 'mp_preference_id')),
        }),
        ('Status do pedido', {
            'fields': (('status', 'reviewed'), ('created_at', 'updated_at')),
        }),
    )

    # --- Painel-resumo do cliente (tudo num cartão visual) ---
    def customer_panel(self, obj):
        if not obj or not obj.pk:
            return "Salve o pedido para ver a ficha completa."

        # WhatsApp: limpa o telefone pra link wa.me
        phone_digits = ''.join(c for c in (obj.customer_phone or '') if c.isdigit())
        wa = f"https://wa.me/55{phone_digits}" if phone_digits else ''

        # itens do pedido
        itens_html = ''
        for it in obj.items.all():
            nome = getattr(getattr(it.variant, 'product', None), 'name', '') or '—'
            tam = getattr(it.variant, 'size_label', '') or ''
            itens_html += (
                f'<tr>'
                f'<td style="padding:4px 10px 4px 0;">{nome} <span style="color:#64748b;">{tam}</span></td>'
                f'<td style="padding:4px 10px;text-align:center;color:#475569;">{it.quantity}x</td>'
                f'<td style="padding:4px 0;text-align:right;font-weight:600;">R$ {it.price}</td>'
                f'</tr>'
            )
        if not itens_html:
            itens_html = '<tr><td colspan="3" style="color:#94a3b8;padding:6px 0;">Sem itens.</td></tr>'

        cfg = STATUS_CFG.get(obj.status, ('#e5e7eb', '#374151', ''))
        status_bg, status_fg, status_svg = cfg

        wa_btn = (
            f'<a href="{wa}" target="_blank" style="display:inline-flex;align-items:center;gap:5px;'
            f'background:#25D366;color:#fff;padding:6px 13px;border-radius:8px;font-weight:700;'
            f'font-size:12px;text-decoration:none;margin-top:4px;">WhatsApp: {obj.customer_phone}</a>'
        ) if wa else f'<span style="color:#94a3b8;">{obj.customer_phone or "sem telefone"}</span>'

        endereco = (obj.shipping_address or '').replace('\n', '<br>') or '<span style="color:#94a3b8;">não informado</span>'
        cep = obj.shipping_cep or '—'

        return format_html(
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;max-width:840px;'
            'background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;padding:20px;">'

            # Coluna 1: cliente + contato
            '<div>'
            '<div style="font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#94a3b8;margin-bottom:6px;">Cliente</div>'
            '<div style="font-size:18px;font-weight:800;color:#0f172a;margin-bottom:2px;">{}</div>'
            '<div style="color:#475569;font-size:13px;margin-bottom:8px;">{}</div>'
            '{}'
            '<div style="margin-top:14px;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#94a3b8;margin-bottom:4px;">Entrega</div>'
            '<div style="font-size:13px;color:#334155;line-height:1.5;"><strong>CEP:</strong> {}<br>{}</div>'
            '</div>'

            # Coluna 2: pedido + status + itens
            '<div>'
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">'
            '<div><div style="font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#94a3b8;">Pedido</div>'
            '<div style="font-size:18px;font-weight:800;color:#0f172a;">#{}</div></div>'
            '<span style="background:{};color:{};padding:4px 12px;border-radius:999px;font-size:11px;font-weight:700;display:inline-flex;align-items:center;">{}{}</span>'
            '</div>'
            '<table style="width:100%;font-size:13px;border-collapse:collapse;margin-bottom:10px;">{}</table>'
            '<div style="border-top:1px solid #e2e8f0;padding-top:8px;display:flex;justify-content:space-between;font-size:13px;color:#475569;">'
            '<span>Frete</span><span>R$ {}</span></div>'
            '<div style="display:flex;justify-content:space-between;font-size:16px;font-weight:800;color:#0f172a;margin-top:2px;">'
            '<span>Total</span><span>R$ {}</span></div>'
            '<div style="margin-top:8px;font-size:12px;color:#94a3b8;">Pedido feito em {}</div>'
            '</div>'

            '</div>',
            obj.customer_name, obj.customer_email, format_html(wa_btn),
            cep, format_html(endereco),
            obj.id, status_bg, status_fg, format_html(status_svg), obj.get_status_display(),
            format_html(itens_html), obj.shipping_cost, obj.total,
            obj.created_at.strftime('%d/%m/%Y às %H:%M') if obj.created_at else '—',
        )
    customer_panel.short_description = ''

    # --- Badge: Novo / Visto ---
    def review_badge(self, obj):
        if obj.reviewed:
            return format_html(
                '<span style="display:inline-flex;align-items:center;gap:4px;background:#f0fdf4;color:#15803d;'
                'padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600;">'
                '<svg width="11" height="11" fill="none" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">'
                '<polyline points="20 6 9 17 4 12"/></svg>Visto</span>'
            )
        return format_html(
            '<span style="display:inline-flex;align-items:center;gap:4px;background:#fef3c7;color:#92400e;'
            'padding:2px 8px;border-radius:999px;font-size:11px;font-weight:700;">'
            '<svg width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" '
            'stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">'
            '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/>'
            '<line x1="12" y1="16" x2="12.01" y2="16"/></svg>Novo</span>'
        )
    review_badge.short_description = ''
    review_badge.admin_order_field = 'reviewed'

    # --- Badge de status colorido ---
    def colored_status(self, obj):
        cfg = STATUS_CFG.get(obj.status)
        if cfg:
            bg, fg, svg = cfg
        else:
            bg, fg, svg = '#e5e7eb', '#374151', ''
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:999px;'
            'font-size:11px;font-weight:600;display:inline-flex;align-items:center;">{}{}</span>',
            bg, fg, format_html(svg), obj.get_status_display()
        )
    colored_status.short_description = 'Status'
    colored_status.admin_order_field = 'status'

    # --- Ações ---
    @admin.action(description='Marcar selecionados como Revisados')
    def marcar_revisado(self, request, queryset):
        updated = queryset.update(reviewed=True)
        self.message_user(request, f"{updated} pedido(s) marcados como revisados.")

    @admin.action(description='Desmarcar Revisado (voltar para Novo)')
    def desmarcar_revisado(self, request, queryset):
        updated = queryset.update(reviewed=False)
        self.message_user(request, f"{updated} pedido(s) redefinidos como Novo.")

    @admin.action(description='Enviar para o Kanban de Triagem')
    def enviar_para_kanban(self, request, queryset):
        updated = queryset.update(status='pago', reviewed=True)
        self.message_user(request, f"{updated} pedido(s) enviados para o Kanban com sucesso!")

    @admin.action(description='Imprimir Ordens de Servico (Selecionadas)')
    def print_os(self, request, queryset):
        orders = queryset.prefetch_related('items__variant__product')
        return TemplateResponse(request, 'admin/orders/order/os_print.html', {'orders': orders})

    def save_model(self, request, obj, form, change):
        if change:
            old = Order.objects.get(pk=obj.pk)
            if old.status != 'enviado' and obj.status == 'enviado':
                super().save_model(request, obj, form, change)
                send_order_shipped_email(obj)
                return
        super().save_model(request, obj, form, change)


# ---------------------------------------------------------------------------
# OrderItemAdmin
# ---------------------------------------------------------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display  = ['id', 'order', 'variant', 'quantity', 'price', 'art_status', 'art_download']
    list_filter   = ['art_status', 'order__status']
    search_fields = ['order__customer_name', 'order__customer_email', 'variant__product__name', 'variant__sku']
    raw_id_fields = ['order', 'variant']
    readonly_fields = ['art_download', 'art_approval_link', 'art_rejection_reason']
    fields        = ['order', 'variant', 'quantity', 'price', 'art_file', 'art_download', 'art_status', 'art_rejection_reason', 'art_approval_link']

    def art_download(self, obj):
        if obj.art_file:
            return format_html('<a href="{}" target="_blank" style="color:#2563eb;font-weight:600;">Baixar arte</a>', obj.art_file.url)
        return "Sem arquivo"
    art_download.short_description = "Arquivo da Arte"

    def art_approval_link(self, obj):
        if not obj.pk:
            return "Salve o item primeiro"
        url = reverse('orders:art_approval', kwargs={'token': obj.art_approval_token})
        send_url = reverse('orders:send_art_approval_email', kwargs={'item_id': obj.pk})
        return format_html(
            '<a href="{}" target="_blank" style="color:#4f46e5;font-weight:600;font-size:12px;">Abrir portal do cliente</a>'
            ' &nbsp;|&nbsp; '
            '<a href="{}" style="color:#16a34a;font-weight:600;font-size:12px;">Enviar por e-mail</a>',
            url, send_url
        )
    art_approval_link.short_description = "Portal de Aprovacao"


# ---------------------------------------------------------------------------
# Painel Kanban (atalho no menu)
# ---------------------------------------------------------------------------
@admin.register(PainelDeProducao)
class PainelDeProducaoAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect('orders:kanban')


# Dashboard atalho
from .models import PainelDeProducao
from .dashboard import dashboard_view as _dbv

class DashboardProxy(Order):
    class Meta:
        proxy = True
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboard"

try:
    admin.site.unregister(DashboardProxy)
except admin.sites.NotRegistered:
    pass

@admin.register(DashboardProxy)
class DashboardAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect('orders:dashboard')


# ---------------------------------------------------------------------------
# Configuração de Frete
# ---------------------------------------------------------------------------
@admin.register(ShippingConfig)
class ShippingConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Melhor Envio API', {
            'fields': ('melhor_envio_token', 'is_sandbox', 'cep_origem', 'dias_adicionais')
        }),
        ('Frete Local / Motoboy (Plano B)', {
            'fields': ('enable_local_delivery', 'local_city', 'local_price')
        }),
    )

    def has_add_permission(self, request):
        return not ShippingConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

