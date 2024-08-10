from django.urls import path

from .views import ProductListApiView, ProductDetailApiView, ProductReviewApiView

urlpatterns = [
    path('product/review/<str:id>', view=ProductReviewApiView.as_view(), name="product_review"),
    path('', view=ProductListApiView.as_view(), name="products"),
    path('product/<str:id>/', view=ProductDetailApiView.as_view(), name="product_detail"),
]