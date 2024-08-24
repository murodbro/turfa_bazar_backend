from rest_framework import serializers

from category.serializers import ProductCategorySerializer, SubProductCategorySerializer
from user.serializers import UserProfileSerializer

from .models import Product, ProductGallery
from store.models import ProductReview, ProductVariation, VariationValue, VariationType


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
        fields = ["id", "name", "description", "image", "category", "subcategory", "gallery", "base_price"]


class VariationValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationValue
        fields = ["id", "type", "value"]


class VariationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationType
        fields = ["id", "name"]


class ProductVariationSerializer(serializers.ModelSerializer):
    variation_values = VariationValueSerializer(many=True)

    class Meta:
        model = ProductVariation
        fields = ["id", "product", "variation_values", "price", "stock"]


class ProductDetailSerializers(serializers.ModelSerializer):
    gallery = ProductGallerySerializer(many=True)
    variations = ProductVariationSerializer(many=True, read_only=True)
    variation_types = VariationTypeSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "image",
            "is_available",
            "details",
            "gallery",
            "ordered_count",
            "variations",
            "owner",
            "variation_types",
            "base_price",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = ProductReview
        fields = ["id", "review", "image", "created_at", "user"]
