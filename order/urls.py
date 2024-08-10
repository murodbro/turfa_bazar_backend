from django.urls import path
from .views import OrderApiView, OrderDetailView, CancelOrderApiView, OrdersHistoryView, CancelOrderStatusApiView, ConfirmSMTPApiView

urlpatterns = [
    path('history/', OrdersHistoryView.as_view(), name='orders_history'),
    path('confirm_smtp/', ConfirmSMTPApiView.as_view(), name='confirm_smtp'),
    path('cancel_order/<str:order_id>/', CancelOrderApiView.as_view(), name='cancel_order'),
    path('change_order_status/<str:order_id>/', CancelOrderStatusApiView.as_view(), name='cancel_order_status'),
    path('order_detail/<str:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path("<str:user_id>/", view=OrderApiView.as_view(), name="order"),
]
