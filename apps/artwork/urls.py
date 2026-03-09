from django.urls import path
from . import views

app_name = 'artwork'

urlpatterns = [
    path('pedido/<int:order_id>/enviar-arte/', views.upload_artwork, name='upload'),
]
