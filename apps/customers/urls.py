from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('painel/', views.my_account, name='dashboard'),
    path('meus-pedidos/', views.my_orders, name='orders'),
    path('pedido/<int:order_id>/', views.order_detail, name='order_detail'),
    path('upload-arte/<int:item_id>/', views.upload_art, name='upload_art'),
]
