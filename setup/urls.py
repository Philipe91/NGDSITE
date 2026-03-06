"""
URL Configuration principal — NGD Site (Web-to-Print)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # As rotas de cada app serão adicionadas aqui nas próximas fases.
    # Exemplo: path("", include("apps.pages.urls")),
]

# Serve arquivos estáticos e de mídia durante o desenvolvimento (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
