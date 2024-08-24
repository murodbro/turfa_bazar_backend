from rest_framework import serializers

from store.serializers import ProductVariationSerializer

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    base_price = serializers.SerializerMethodField()
    product_variation = ProductVariationSerializer()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "user",
            "product",
            "quantity",
            "sub_total",
            "image",
            "base_price",
            "product_id",
            "product_variation",
        ]

    def get_product(self, obj):
        return obj.product.name

    def get_product_id(self, obj):
        return obj.product.id

    def get_stock(self, obj):
        return obj.product.stock

    def get_base_price(self, obj):
        return obj.product.base_price

    def get_image(self, obj):
        request = self.context.get("request")
        image_url = obj.product.image.url
        return request.build_absolute_uri(image_url) if request else image_url
