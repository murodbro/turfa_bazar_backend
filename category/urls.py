from django.urls import path

from .views import AllProductCategoryApiView, ProductCategoryApiView


urlpatterns = [
    path("", view=AllProductCategoryApiView.as_view(), name="category"),
    path("<str:slug>/", view=ProductCategoryApiView.as_view(), name="product_category"),
]