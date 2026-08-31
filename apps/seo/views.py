from django.shortcuts import render
from django.http import HttpResponse
from apps.catalog.models import Product, Category
from apps.pages.models import Page
from django.urls import reverse
from django.conf import settings

def _lastmod(obj):
    """Data da ultima alteracao, usada pelo Google para decidir o recrawl."""
    data = getattr(obj, "updated_at", None) or getattr(obj, "created_at", None)
    return data.date().isoformat() if data else None


def robots_txt(request):
    prefixo = getattr(settings, "FORCE_SCRIPT_NAME", "") or ""
    lines = [
        "User-agent: *",
        "Disallow: " + prefixo + "/admin/",
        "Disallow: " + prefixo + "/accounts/",
        "Disallow: " + prefixo + "/carrinho/",
        "Disallow: " + prefixo + "/cliente/",
        "Disallow: " + prefixo + "/pagamento/",
        "Disallow: " + prefixo + "/pedidos/",
        "Sitemap: " + request.build_absolute_uri(reverse("seo:sitemap_xml")),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def sitemap_xml(request):
    urls = []
    
    # Adicionar Home
    urls.append({'loc': request.build_absolute_uri(reverse('catalog:home')), 'changefreq': 'daily', 'priority': '1.0'})
    
    # Produtos
    for product in Product.objects.filter(is_active=True):
        loc = request.build_absolute_uri(product.get_absolute_url() if hasattr(product, 'get_absolute_url') else f"/produto/{product.slug}/")
        urls.append({'loc': loc, 'changefreq': 'weekly', 'priority': '0.9', 'lastmod': _lastmod(product)})
        
    # Categorias
    for category in Category.objects.filter(is_active=True):
        loc = request.build_absolute_uri(category.get_absolute_url() if hasattr(category, 'get_absolute_url') else f"/categoria/{category.slug}/")
        urls.append({'loc': loc, 'changefreq': 'weekly', 'priority': '0.8', 'lastmod': _lastmod(category)})
        
    # Páginas
    for page in Page.objects.filter(is_active=True):
        loc = request.build_absolute_uri(reverse('pages:page_detail', kwargs={'slug': page.slug}))
        urls.append({'loc': loc, 'changefreq': 'monthly', 'priority': '0.5', 'lastmod': _lastmod(page)})
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml.append('  <url>')
        xml.append(f"    <loc>{u['loc']}</loc>")
        if u.get('lastmod'):
            xml.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        xml.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        xml.append(f"    <priority>{u['priority']}</priority>")
        xml.append('  </url>')
    xml.append('</urlset>')
    
    return HttpResponse("\n".join(xml), content_type="application/xml")
