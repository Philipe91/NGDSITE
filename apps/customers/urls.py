from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('painel/', views.my_account, name='dashboard'),
    path('meus-pedidos/', views.my_orders, name='orders'),
]
