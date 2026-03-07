from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('contato/', views.contact_view, name='contact'),
    path('<slug:slug>/', views.page_detail, name='page_detail'),
]
