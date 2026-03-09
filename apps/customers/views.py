from django.shortcuts import render, redirect
from django.contrib import messages
from apps.orders.models import Order

CUSTOMER_SESSION_KEY = 'customer_email'


def _require_customer(request):
    """Retorna o email da sessão ou None se não logado."""
    return request.session.get(CUSTOMER_SESSION_KEY)


def login_view(request):
    """Login simples por e-mail (sem senha, baseado em pedidos existentes)."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if Order.objects.filter(customer_email__iexact=email).exists():
            request.session[CUSTOMER_SESSION_KEY] = email
            return redirect('customers:dashboard')
        else:
            messages.error(request, 'Nenhum pedido encontrado para este e-mail. Verifique o e-mail usado no checkout.')
    return render(request, 'customers/login.html')


def logout_view(request):
    """Limpa a sessão do cliente."""
    request.session.pop(CUSTOMER_SESSION_KEY, None)
    return redirect('catalog:home')


def my_account(request):
    """Painel do cliente — resumo dos pedidos."""
    email = _require_customer(request)
    if not email:
        return redirect('customers:login')

    orders = Order.objects.filter(customer_email__iexact=email).order_by('-created_at')
    active_count = orders.exclude(status='entregue').count()
    total_count = orders.count()

    context = {
        'customer_email': email,
        'customer_name': orders.first().customer_name if orders.exists() else email,
        'orders': orders[:5],
        'active_count': active_count,
        'total_count': total_count,
    }
    return render(request, 'customers/my_account.html', context)


def my_orders(request):
    """Lista completa de pedidos do cliente."""
    email = _require_customer(request)
    if not email:
        return redirect('customers:login')

    orders = Order.objects.filter(customer_email__iexact=email).prefetch_related('items__variant__product').order_by('-created_at')
    context = {
        'customer_email': email,
        'customer_name': orders.first().customer_name if orders.exists() else email,
        'orders': orders,
    }
    return render(request, 'customers/my_orders.html', context)
