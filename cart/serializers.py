from operator import truediv
from rest_framework import serializers

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "user", "product", "quantity", "sub_total", "image", "stock", "price", "product_id"]

    def get_product(self, obj):
        return obj.product.name

    def get_product_id(self, obj):
        return obj.product.id

    def get_stock(self, obj):
        return obj.product.stock

    def get_price(self, obj):
        return obj.product.price

    def get_image(self, obj):
        request = self.context.get("request")
        image_url = obj.product.image.url
        return request.build_absolute_uri(image_url) if request else image_url