from django.urls import path
from . import views
from .dashboard import dashboard_view
from .art_approval import art_approval_view, art_approve, art_reject, send_art_approval_email_view

app_name = 'orders'

urlpatterns = [
    # Checkout / pedido
    path('finalizar/', views.checkout, name='checkout'),
    path('sucesso/<int:order_id>/', views.checkout_success, name='checkout_success'),
    path('<int:order_id>/itens/<int:item_id>/upload-arte/', views.upload_art, name='upload_art'),
    path('calcular-frete/', views.calcular_frete, name='calcular_frete'),

    # Kanban
    path('kanban/', views.kanban_view, name='kanban'),
    path('kanban/update-status/', views.update_order_status, name='update_order_status'),

    # Dashboard (admin)
    path('dashboard/', dashboard_view, name='dashboard'),

    # Portal de Aprovacao de Arte (publico com token)
    path('arte/aprovar/<uuid:token>/', art_approval_view, name='art_approval'),
    path('arte/aprovar/<uuid:token>/ok/', art_approve, name='art_approve'),
    path('arte/aprovar/<uuid:token>/rejeitar/', art_reject, name='art_reject'),

    # Acao admin: enviar email de aprovacao
    path('arte/enviar-email/<int:item_id>/', send_art_approval_email_view, name='send_art_approval_email'),
]
