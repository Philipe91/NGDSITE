from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from apps.cart.cart import Cart
from .models import Order, OrderItem
from .shipping import get_shipping_options
from .emails import send_order_created_email, send_status_update_email, send_order_shipped_email
from decimal import Decimal

CUSTOMER_SESSION_KEY = 'customer_email'
CUSTOMER_SESSION_VERIFIED_KEY = 'customer_email_verified'  # marcado True após criar pedido
ALLOWED_ART_EXTENSIONS = {'.pdf', '.cdr', '.ai', '.jpg', '.jpeg', '.png'}
ALLOWED_ART_MIME_TYPES = {
    'application/pdf',
    'application/postscript',          # .ai
    'application/illustrator',         # .ai
    'image/x-coreldraw', 'application/x-coreldraw', 'application/cdr',
    'application/octet-stream',        # .cdr/.ai costumam vir genéricos
    'image/jpeg', 'image/pjpeg',
    'image/png',
}
# Magic bytes para confirmar tipo real (defesa contra malware.exe.pdf)
ART_MAGIC_BYTES = {
    '.pdf': [b'%PDF-'],
    '.jpg': [b'\xff\xd8\xff'],
    '.jpeg': [b'\xff\xd8\xff'],
    '.png': [b'\x89PNG\r\n\x1a\n'],
    '.ai': [b'%PDF-', b'%!PS-Adobe'],   # AI moderno é PDF; antigo é PostScript
    '.cdr': [b'RIFF', b'PK\x03\x04'],   # CDR antigo (RIFF) ou novo (zip)
}


def _can_manage_order_art(request, order):
    """Permite gerenciar arte se: staff, dono autenticado, OU sessão com email
    verificado (marcada após o checkout) que bate com o pedido."""
    if request.user.is_staff:
        return True

    if request.user.is_authenticated and request.user.email:
        if request.user.email.strip().lower() == order.customer_email.strip().lower():
            return True

    # Sessão de convidado — só vale se foi marcada como verificada no checkout
    if request.session.get(CUSTOMER_SESSION_VERIFIED_KEY):
        customer_email = request.session.get(CUSTOMER_SESSION_KEY, '').strip().lower()
        if customer_email and customer_email == order.customer_email.strip().lower():
            return True

    return False


def _quantity_discount_multiplier(quantity):
    """Mesma regra do cart_add — fonte única no servidor."""
    if quantity >= 10:
        return Decimal('0.85')
    if quantity >= 5:
        return Decimal('0.90')
    if quantity >= 2:
        return Decimal('0.95')
    return Decimal('1.00')


def _validate_file_signature(uploaded_file, extension):
    """Confere magic bytes do arquivo contra a extensão declarada."""
    expected = ART_MAGIC_BYTES.get(extension)
    if not expected:
        return True  # extensão sem assinatura conhecida, deixa passar (já validamos lista branca)
    head = uploaded_file.read(16)
    uploaded_file.seek(0)
    return any(head.startswith(sig) for sig in expected)


@ratelimit(key='ip', rate='60/m', block=True)
def calcular_frete(request):
    """Endpoint AJAX — retorna opções de frete para o CEP informado."""
    cep = request.GET.get('cep', '').replace('-', '').strip()
    if len(cep) != 8 or not cep.isdigit():
        return JsonResponse({'error': 'CEP inválido. Informe 8 dígitos.'}, status=400)

    cart = Cart(request)
    options = get_shipping_options(cep, cart)
    return JsonResponse({
        'options': [
            {
                'id': o['id'],
                'label': o['label'],
                'description': o['description'],
                'cost': float(o['cost']),
                'days': o['days'],
            }
            for o in options
        ]
    })


def _compute_unit_price(variant, quantity, prazo):
    """Fonte única do preço unitário no servidor — espelha apps/cart/views.cart_add."""
    base_price = Decimal(str(variant.price))
    discount = _quantity_discount_multiplier(quantity)

    express_fee = Decimal('0.00')
    if variant.product.slug == 'banner-rollup':
        express_fee = {6: Decimal('20'), 5: Decimal('40'), 4: Decimal('60'),
                       3: Decimal('80'), 2: Decimal('100')}.get(int(prazo or 0), Decimal('0'))

    return (base_price * discount).quantize(Decimal('0.01')) + express_fee


@ratelimit(key='ip', rate='30/m', method='POST', block=True)
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('catalog:home')

    if request.method == 'POST':
        name = request.POST.get('customer_name', '').strip()[:200]
        email = request.POST.get('customer_email', '').strip().lower()[:254]
        phone = request.POST.get('customer_phone', '').strip()[:30]
        shipping_method = request.POST.get('shipping_method', 'retirada').strip()[:80]
        shipping_cep = request.POST.get('shipping_cep', '').strip()[:9]
        shipping_address = request.POST.get('shipping_address', '').strip()[:500]

        if not name or '@' not in email:
            messages.error(request, 'Informe nome e e-mail válidos.')
            return redirect('orders:checkout')

        # ---------------------------------------------------------------
        # FRETE — recalcular no servidor; cliente NÃO define o valor
        # ---------------------------------------------------------------
        shipping_cost = Decimal('0.00')
        if shipping_method.lower() in ('retirada', 'retirada na loja'):
            shipping_cost = Decimal('0.00')
            shipping_method = 'Retirada na Loja'
        elif shipping_cep and len(shipping_cep.replace('-', '')) == 8:
            options = get_shipping_options(shipping_cep, cart)
            chosen = next(
                (o for o in options if o['id'] == shipping_method or o['label'] == shipping_method),
                None,
            )
            if chosen:
                shipping_cost = Decimal(str(chosen['cost']))
                shipping_method = chosen['label']
            else:
                messages.error(request, 'Opção de frete inválida. Recalcule o frete.')
                return redirect('orders:checkout')
        else:
            messages.error(request, 'Informe um CEP válido para entrega.')
            return redirect('orders:checkout')

        # ---------------------------------------------------------------
        # ITENS — recalcular preço a partir do banco (NÃO confiar na sessão)
        # ---------------------------------------------------------------
        try:
            with transaction.atomic():
                subtotal = Decimal('0.00')
                items_to_create = []

                for item in cart:
                    variant = item['variant']
                    if not variant.is_active:
                        raise ValueError(f'Produto "{variant.product.name}" indisponível.')

                    quantity = max(1, min(999, int(item['quantity'])))
                    prazo = int(item.get('prazo') or 0)
                    unit_price = _compute_unit_price(variant, quantity, prazo)
                    line_total = unit_price * quantity
                    subtotal += line_total

                    items_to_create.append({
                        'variant': variant,
                        'price': unit_price,
                        'quantity': quantity,
                    })

                total = subtotal + shipping_cost

                order = Order.objects.create(
                    customer_name=name,
                    customer_email=email,
                    customer_phone=phone,
                    shipping_method=shipping_method,
                    shipping_cost=shipping_cost,
                    shipping_cep=shipping_cep,
                    shipping_address=shipping_address,
                    subtotal=subtotal,
                    total=total,
                )

                for it in items_to_create:
                    OrderItem.objects.create(order=order, **it)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('orders:checkout')
        except Exception:
            import logging
            logging.getLogger(__name__).exception('Falha no checkout')
            messages.error(request, 'Não foi possível concluir o pedido. Tente novamente.')
            return redirect('orders:checkout')

        cart.clear()

        # Sessão de convidado — marca como verificada SÓ AGORA, depois de criar pedido válido
        request.session[CUSTOMER_SESSION_KEY] = email
        request.session[CUSTOMER_SESSION_VERIFIED_KEY] = True
        request.session.set_expiry(60 * 60 * 24 * 7)  # 7 dias

        send_order_created_email(order)

        return redirect('payment:pay', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


def checkout_success(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__variant__product'), id=order_id)
    return render(request, 'orders/success.html', {'order': order})


@ratelimit(key='ip', rate='20/m', method='POST', block=True)
def upload_art(request, order_id, item_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    order = get_object_or_404(Order.objects.prefetch_related('items'), id=order_id)
    item = get_object_or_404(OrderItem, id=item_id, order=order)

    if not _can_manage_order_art(request, order):
        return JsonResponse({'error': 'Você não tem permissão para enviar arte para este pedido.'}, status=403)

    uploaded_file = request.FILES.get('art_file')
    if not uploaded_file:
        return JsonResponse({'error': 'Selecione um arquivo para enviar.'}, status=400)

    # 1) Tamanho — bloqueia DoS por upload gigante
    max_bytes = getattr(settings, 'ART_UPLOAD_MAX_BYTES', 50 * 1024 * 1024)
    if uploaded_file.size > max_bytes:
        return JsonResponse({
            'error': f'Arquivo excede o limite de {max_bytes // (1024 * 1024)} MB.'
        }, status=400)

    # 2) Extensão — lista branca
    file_name = uploaded_file.name.lower()
    extension = f".{file_name.rsplit('.', 1)[-1]}" if '.' in file_name else ''
    if extension not in ALLOWED_ART_EXTENSIONS:
        return JsonResponse({
            'error': 'Formato inválido. Envie PDF, CDR, AI, JPG ou PNG.'
        }, status=400)

    # 3) Content-Type declarado pelo browser — defesa em camadas
    declared_type = (uploaded_file.content_type or '').lower()
    if declared_type and declared_type not in ALLOWED_ART_MIME_TYPES:
        return JsonResponse({
            'error': 'Tipo de arquivo inválido (content-type).'
        }, status=400)

    # 4) Magic bytes — confirma que o conteúdo bate com a extensão
    if not _validate_file_signature(uploaded_file, extension):
        return JsonResponse({
            'error': 'O conteúdo do arquivo não corresponde ao formato declarado.'
        }, status=400)

    # Sanitiza nome do arquivo (Django já faz, mas reforça contra path traversal)
    import os.path
    safe_name = os.path.basename(uploaded_file.name).replace('\\', '_').replace('/', '_')
    uploaded_file.name = safe_name

    item.art_file = uploaded_file
    item.art_status = 'em_analise'
    item.save(update_fields=['art_file', 'art_status'])

    if order.status in {'aguardando_pagamento', 'pago', 'aguardando_arte'}:
        order.status = 'arte_recebida'
        order.save(update_fields=['status'])

    return JsonResponse({
        'success': True,
        'message': 'Arte enviada com sucesso. Nosso time já está analisando.',
        'file_name': item.art_file.name.split('/')[-1],
        'file_url': item.art_file.url,
        'art_status': item.get_art_status_display(),
    })


import json
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

@staff_member_required
def kanban_view(request):
    """View do Kanban Board de Produção"""
    # Vamos pegar todos os pedidos, menos os cancelados e aguardando_pagamento (ainda não entraram)
    qs = Order.objects.exclude(status__in=['cancelado', 'aguardando_pagamento']).prefetch_related('items__variant__product').order_by('created_at')
    
    orders_data = []
    for o in qs:
        orders_data.append({
            'id': o.id,
            'status': o.status,
            'customer': o.customer_name,
            'date': o.created_at.isoformat(),
            'total': float(o.total),
            'items': [{'name': i.variant.product.name if i.variant else 'Produto Genérico', 'qtd': i.quantity} for i in o.items.all()]
        })
        
    return render(request, 'admin/kanban.html', {'orders_data': orders_data})

@staff_member_required
@require_POST
def update_order_status(request):
    """Endpoint AJAX para atualizar status arrastando no Kanban"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        new_status = data.get('status')
        
        order = get_object_or_404(Order, id=order_id)
        if new_status in dict(Order.STATUS_CHOICES):
            # Only send email if status actually changed
            if order.status != new_status:
                order.status = new_status
                order.save(update_fields=['status'])
                
                # Dispara emails baseado no novo status
                if new_status == 'arte_recebida':
                    send_status_update_email(order, "Sua arte foi Aprovada e o pedido está pronto para produção.")
                elif new_status == 'em_producao':
                    send_status_update_email(order, "Seu pedido entrou em Produção!")
                elif new_status == 'enviado':
                    send_order_shipped_email(order)
                    
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Status inválido.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

