from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('<int:order_id>/', views.pay, name='pay'),
    path('webhook/', views.webhook, name='webhook'),
]
