from django.db.models import ForeignKey, CASCADE, IntegerField

from core.models import Model
from store.models import Product
from user.models import Account



class CartItem(Model):
    user = ForeignKey(Account, on_delete=CASCADE, null=True)
    product = ForeignKey(Product, on_delete=CASCADE, related_name='cart')
    quantity = IntegerField()

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return self.product.name

