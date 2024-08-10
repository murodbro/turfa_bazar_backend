from rest_framework import generics

from .serializers import ProductCategorySerializer
from .models import ProductCategory


class ProductCategoryApiView(generics.ListAPIView):
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        return ProductCategory.objects.filter(slug=self.kwargs["slug"])

class AllProductCategoryApiView(generics.ListAPIView):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
