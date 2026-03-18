"""
Dashboard views — Fase 15
"""
import json
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDate
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone

from apps.orders.models import Order, OrderItem


# ─── Paleta de badges por status ─────────────────────────────────────────────
STATUS_BADGES = {
    'aguardando_pagamento': ('#f1f5f9', '#64748b', '#e2e8f0'),
    'pago':                 ('#dbeafe', '#1e40af', '#bfdbfe'),
    'aguardando_arte':      ('#fff7ed', '#9a3412', '#fed7aa'),
    'arte_recebida':        ('#fef9c3', '#854d0e', '#fde68a'),
    'em_producao':          ('#ede9fe', '#4c1d95', '#ddd6fe'),
    'enviado':              ('#dcfce7', '#14532d', '#bbf7d0'),
    'entregue':             ('#d1fae5', '#064e3b', '#6ee7b7'),
    'cancelado':            ('#fee2e2', '#7f1d1d', '#fecaca'),
}

STATUS_LABELS = dict(Order.STATUS_CHOICES)


# ─── DASHBOARD ────────────────────────────────────────────────────────────────
@staff_member_required
def dashboard_view(request):
    today        = timezone.now().date()
    month_start  = today.replace(day=1)
    thirty_ago   = today - timedelta(days=29)

    paid_qs = Order.objects.filter(
        status__in=['pago', 'arte_recebida', 'aguardando_arte', 'em_producao', 'enviado', 'entregue']
    )

    # KPIs básicos
    receita_mes    = paid_qs.filter(created_at__date__gte=month_start).aggregate(t=Sum('total'))['t'] or Decimal('0')
    pedidos_mes    = paid_qs.filter(created_at__date__gte=month_start).count()
    receita_hoje   = paid_qs.filter(created_at__date=today).aggregate(t=Sum('total'))['t'] or Decimal('0')
    pedidos_hoje   = paid_qs.filter(created_at__date=today).count()
    receita_total  = paid_qs.aggregate(t=Sum('total'))['t'] or Decimal('0')
    total_pedidos_pagos = paid_qs.count()
    ticket_medio   = (receita_total / total_pedidos_pagos) if total_pedidos_pagos else Decimal('0')

    # Alertas de triagem
    novos_nao_revisados = Order.objects.filter(status='pago', reviewed=False).count()
    em_producao     = Order.objects.filter(status='em_producao').count()
    aguardando_envio = Order.objects.filter(status='enviado').count()

    # Pipeline por status
    status_counts = []
    for key, label in Order.STATUS_CHOICES:
        bg, color, border = STATUS_BADGES.get(key, ('#f8fafc', '#374151', '#e2e8f0'))
        cnt = Order.objects.filter(status=key).count()
        if cnt > 0:
            status_counts.append({'status': key, 'label': label, 'count': cnt, 'bg': bg, 'color': color, 'border': border})

    # Gráfico - receita últimos 30 dias
    daily = (
        paid_qs
        .filter(created_at__date__gte=thirty_ago)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Sum('total'))
        .order_by('day')
    )
    days_map = {row['day']: float(row['total']) for row in daily}
    chart_labels = []
    chart_data   = []
    for i in range(30):
        d = thirty_ago + timedelta(days=i)
        chart_labels.append(d.strftime('%d/%m'))
        chart_data.append(days_map.get(d, 0))

    # Top 5 produtos
    from apps.catalog.models import ProductVariant
    top_raw = (
        OrderItem.objects
        .filter(order__status__in=['pago', 'arte_recebida', 'aguardando_arte', 'em_producao', 'enviado', 'entregue'])
        .select_related('variant__product')
        .values('variant__product__name')
        .annotate(qty=Sum('quantity'), revenue=Sum('price'))
        .order_by('-revenue')[:5]
    )
    top_products = [{'name': r['variant__product__name'] or 'Produto Removido', 'qty': r['qty'], 'revenue': r['revenue'] or 0} for r in top_raw]

    # Pedidos recentes (10)
    recent_raw = Order.objects.all()[:10]
    recent_orders = []
    for o in recent_raw:
        bg, color, _ = STATUS_BADGES.get(o.status, ('#f1f5f9', '#64748b', '#e2e8f0'))
        o.badge_bg    = bg
        o.badge_color = color
        recent_orders.append(o)

    return render(request, 'admin/dashboard.html', {
        'receita_mes':          receita_mes,
        'pedidos_mes':          pedidos_mes,
        'receita_hoje':         receita_hoje,
        'pedidos_hoje':         pedidos_hoje,
        'receita_total':        receita_total,
        'total_pedidos_pagos':  total_pedidos_pagos,
        'ticket_medio':         ticket_medio,
        'novos_nao_revisados':  novos_nao_revisados,
        'em_producao':          em_producao,
        'aguardando_envio':     aguardando_envio,
        'status_counts':        status_counts,
        'chart_labels':         json.dumps(chart_labels),
        'chart_data':           json.dumps(chart_data),
        'top_products':         top_products,
        'recent_orders':        recent_orders,
    })
