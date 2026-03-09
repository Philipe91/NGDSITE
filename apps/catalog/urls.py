from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('categoria/<slug:slug>/', views.category_detail, name='category_detail'),
    path('produto/<slug:slug>/', views.product_detail, name='product_detail'),
]
