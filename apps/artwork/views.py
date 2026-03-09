from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.orders.models import Order
from .models import ArtworkFile

CUSTOMER_SESSION_KEY = 'customer_email'


def upload_artwork(request, order_id):
    """View para cliente fazer upload de arte para um pedido."""
    email = request.session.get(CUSTOMER_SESSION_KEY)
    if not email:
        return redirect('customers:login')

    order = get_object_or_404(Order, id=order_id, customer_email__iexact=email)

    if request.method == 'POST':
        file = request.FILES.get('artwork_file')
        notes = request.POST.get('notes', '').strip()

        if not file:
            messages.error(request, 'Selecione um arquivo para enviar.')
        else:
            allowed_extensions = ['.pdf', '.ai', '.eps', '.psd', '.png', '.jpg', '.jpeg', '.tif', '.tiff', '.zip']
            file_ext = '.' + file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''
            if file_ext not in allowed_extensions:
                messages.error(request, f'Formato não suportado. Envie arquivos: PDF, AI, EPS, PSD, PNG, JPG, TIF ou ZIP.')
            else:
                artwork = ArtworkFile(order=order, file=file, notes=notes, original_name=file.name)
                artwork.save()
                if order.status == 'aguardando_pagamento':
                    order.status = 'aguardando_arte'
                    order.save()
                messages.success(request, f'Arte "{file.name}" enviada com sucesso!')
                return redirect('customers:orders')

    artworks = order.artworks.all()
    context = {
        'order': order,
        'artworks': artworks,
        'customer_email': email,
    }
    return render(request, 'artwork/upload_artwork.html', context)
