from django.shortcuts import render
from django.http import HttpResponse
from apps.catalog.models import Product, Category
from apps.pages.models import Page
from django.urls import reverse

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /carrinho/",
        "Disallow: /cliente/",
        "Disallow: /pagamento/",
        "Disallow: /pedidos/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def sitemap_xml(request):
    urls = []
    
    # Adicionar Home
    urls.append({'loc': request.build_absolute_uri('/'), 'changefreq': 'daily', 'priority': '1.0'})
    
    # Produtos
    for product in Product.objects.filter(is_active=True):
        loc = request.build_absolute_uri(product.get_absolute_url() if hasattr(product, 'get_absolute_url') else f"/produto/{product.slug}/")
        urls.append({'loc': loc, 'changefreq': 'weekly', 'priority': '0.9'})
        
    # Categorias
    for category in Category.objects.filter(is_active=True):
        loc = request.build_absolute_uri(category.get_absolute_url() if hasattr(category, 'get_absolute_url') else f"/categoria/{category.slug}/")
        urls.append({'loc': loc, 'changefreq': 'weekly', 'priority': '0.8'})
        
    # Páginas
    for page in Page.objects.filter(is_active=True):
        loc = request.build_absolute_uri(reverse('pages:page_detail', kwargs={'slug': page.slug}))
        urls.append({'loc': loc, 'changefreq': 'monthly', 'priority': '0.5'})
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml.append('  <url>')
        xml.append(f"    <loc>{u['loc']}</loc>")
        xml.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        xml.append(f"    <priority>{u['priority']}</priority>")
        xml.append('  </url>')
    xml.append('</urlset>')
    
    return HttpResponse("\n".join(xml), content_type="application/xml")
