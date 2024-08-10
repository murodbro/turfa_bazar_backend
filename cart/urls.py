from django.urls import path

from .views import CartItemApiView

urlpatterns = [
    path("cart_items/<str:user_id>/", view=CartItemApiView.as_view(), name="cart_items")
]