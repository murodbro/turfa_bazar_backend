from rest_framework import serializers

from .models import ProductCategory, SubProductCategory


class SubProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubProductCategory
        fields = ["id", "name", "slug"]


class ProductCategorySerializer(serializers.ModelSerializer):
    sub_category = SubProductCategorySerializer(many=True)

    class Meta:
        model = ProductCategory
        fields = ["id", "name", "slug", "sub_category"]

