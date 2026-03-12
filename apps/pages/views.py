from django.shortcuts import render, get_object_or_404
from .models import Page

def contact_view(request):
    if request.method == "POST":
        # Aqui no futuro podemos enviar um email para a loja, por ora só renderiza a página de sucesso
        context = {"sucesso": True}
        return render(request, "pages/contact.html", context)
    return render(request, "pages/contact.html")

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_active=True)
    return render(request, "pages/page_detail.html", {"page": page})
