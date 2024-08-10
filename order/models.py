from django.utils.translation import gettext_lazy as _
from django.db.models import (
                    CharField,
                    ForeignKey,
                    BooleanField,
                    EmailField,
                    IntegerField,
                    DecimalField,
                    TextChoices,
                    CASCADE
                )

from user.models import Account
from core.models import Model
from store.models import Product

class Order(Model):
    user = ForeignKey(Account, on_delete=CASCADE, null=True)

    city = CharField(blank=True, max_length=50)
    state = CharField(blank=True, max_length=50)
    address = CharField(blank=True, max_length=100)
    email = EmailField(blank=True, max_length=100)
    phone = CharField(blank=True, max_length=50)
    order_code = CharField(blank=True, max_length=20, null=True)
    smtp_code = CharField(blank=True, max_length=20, null=True)

    buy_cash = BooleanField(default=False)
    recive_by_deliver =BooleanField(default=False)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self) -> str:
        return self.user.email


class OrderItems(Model):
    class Status_delivary(TextChoices):
        PENDING = 'Kutilmoqda', _('Kutilmoqda...')
        SHIPPED = "Jo'natilinmoqda", _("Jo'natilinmoqda...")
        DELIVERED = 'Yetkazib berildi', _('Yetkazib berildi')
        CANCELED = 'Bekor qilindi', _('Bekor qilindi')

    order = ForeignKey(Order, on_delete=CASCADE, related_name="order_items")
    product = ForeignKey(Product, on_delete=CASCADE)
    status = CharField(choices=Status_delivary.choices, default=Status_delivary.PENDING, max_length=50)
    quantity = IntegerField()
    unit_price = DecimalField(max_digits=9, decimal_places=2)
    confirmed = BooleanField(default=False)

    def sub_total(self):
        return self.quantity * self.unit_price



