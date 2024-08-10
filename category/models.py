from django.db.models import CharField, ForeignKey, CASCADE, SlugField

from core.models import Model


class ProductCategory(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True)

    def __str__(self):
        return self.name


class SubProductCategory(Model):
    category = ForeignKey(ProductCategory, related_name='sub_category', on_delete=CASCADE)
    name = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'category']

