from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('finalizar/', views.checkout, name='checkout'),
    path('sucesso/<int:order_id>/', views.checkout_success, name='checkout_success'),
    path('<int:order_id>/itens/<int:item_id>/upload-arte/', views.upload_art, name='upload_art'),
    path('calcular-frete/', views.calcular_frete, name='calcular_frete'),
]
