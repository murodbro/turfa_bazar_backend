from django.db.models import ForeignKey, CASCADE, IntegerField

from core.models import Model
from store.models import Product, ProductVariation
from user.models import Account


class CartItem(Model):
    user = ForeignKey(Account, on_delete=CASCADE, null=True)
    product = ForeignKey(Product, on_delete=CASCADE, related_name="cart")
    product_variation = ForeignKey(
        ProductVariation, on_delete=CASCADE, null=True, blank=True, related_name="cart_items"
    )
    quantity = IntegerField()

    def sub_total(self):
        price = self.product_variation.price if self.product_variation else self.product.base_price
        return price * self.quantity

    def __str__(self) -> str:
        return f"{self.product.name} ({self.product_variation})" if self.product_variation else self.product.name
