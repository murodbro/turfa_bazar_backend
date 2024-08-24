from rest_framework import serializers

from store.serializers import ProductVariationSerializer
from .models import Order, OrderItems


class OrderItemsSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    product_variation = ProductVariationSerializer()

    class Meta:
        model = OrderItems  # noqa: F811
        fields = [
            "id",
            "order",
            "product",
            "status",
            "quantity",
            "unit_price",
            "sub_total",
            "confirmed",
            "image",
            "description",
            "product_id",
            "product_variation",
        ]

    def get_product(self, obj):
        return obj.product.name

    def get_product_id(self, obj):
        return obj.product.id

    def get_description(self, obj):
        return obj.product.description

    def get_image(self, obj):
        request = self.context.get("request")
        image_url = obj.product.image.url
        return request.build_absolute_uri(image_url) if request else image_url


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "city",
            "state",
            "address",
            "buy_cash",
            "recive_by_deliver",
            "email",
            "order_items",
            "phone",
            "order_code",
            "smtp_code",
        ]


class OrdersHistorySerializers(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "buy_cash", "recive_by_deliver", "order_items", "order_code", "created_at"]
