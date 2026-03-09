"""
URL Configuration principal — NGD Site (Web-to-Print)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "NGD - Painel Administrativo"
admin.site.site_title = "NGD Site Admin"
admin.site.index_title = "Gerenciamento da Gráfica"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("apps.catalog.urls", "catalog"))),
    path("carrinho/", include(("apps.cart.urls", "cart"))),
    path("pedido/", include(("apps.orders.urls", "orders"))),
    path("cliente/", include(("apps.customers.urls", "customers"))),
    path("arte/", include(("apps.artwork.urls", "artwork"))),
]

# Serve arquivos estáticos e de mídia durante o desenvolvimento (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
