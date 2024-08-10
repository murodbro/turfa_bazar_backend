from dataclasses import fields
from rest_framework import serializers

from category.serializers import ProductCategorySerializer, SubProductCategorySerializer
from user.serializers import UserProfileSerializer

from .models import Product, ProductGallery
from store.models import ProductReview, ProductVariation


class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = ["gallery"]


class ProductSerializers(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    subcategory = SubProductCategorySerializer()
    gallery = ProductGallerySerializer(many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "image", "category", "subcategory", "gallery"]


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ["id", "name", "variation", "price"]


class ProductDetailSerializers(serializers.ModelSerializer):
    gallery = ProductGallerySerializer(many=True)
    variation = VariationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "image", "is_available", "stock", "details", "gallery", "ordered_count", "variation", "owner"]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = ProductReview
        fields = ["id", "review", "image", "created_at", "user"]
