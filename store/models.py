from django.db.models import (
            CharField,
            DecimalField,
            IntegerField,
            ImageField,
            BooleanField,
            TextField,
            ForeignKey,
            CASCADE,
            SET_NULL,
            TextChoices
            )
from django.utils.translation import gettext_lazy as _
from core.models import Model
from category.models import ProductCategory, SubProductCategory
from user.models import Account


class Product(Model):
    category = ForeignKey(ProductCategory, related_name='product', on_delete=CASCADE, null=True, blank=True)
    subcategory = ForeignKey(SubProductCategory, related_name='product', on_delete=CASCADE, null=True, blank=True)
    name = CharField(max_length=255)
    description = CharField(max_length=355)
    owner = CharField(max_length=255, null=True, blank=True)
    image = ImageField(upload_to='photos/products', null=True)
    stock = IntegerField(default=0)
    ordered_count = IntegerField(default=0)
    is_available = BooleanField(default=True)
    details = TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class ProductGallery(Model):
    product = ForeignKey(Product, related_name='gallery', on_delete=CASCADE)
    gallery = ImageField(upload_to='photos/products', null=True)

    def __str__(self):
        return self.product.name + " " + self.gallery.name


class ProductReview(Model):
    product = ForeignKey(Product, on_delete=CASCADE, related_name="review")
    user = ForeignKey(Account, on_delete=SET_NULL, related_name="review", null=True, blank=True)
    review = CharField(max_length=255)
    image = ImageField(upload_to="photos/reviews", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.product.name} - {self.review}"


class ProductVariation(Model):

    class VariationType(TextChoices):
        SIZE = "O'lchami", _("O'lchami")
        COLOR = 'Rangi', _('Rangi')
        VOLUME = "Hajmi", _("Hajmi")
        MEMORY = "Xotirasi", _("Xotirasi")
        WEIGHT = "Og'irligi", _("Og'irligi")

    product = ForeignKey(Product, on_delete=CASCADE, related_name="variation", null=True)
    name = CharField(max_length=255, null=True, blank=True, choices=VariationType.choices)
    variation = CharField(max_length=255, null=True, blank=True)
    price = DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self) -> str:
        return f"{self.product.name} - {self.name} - {self.variation}"
