from django.contrib import admin

from .models import Product, ProductGallery, ProductReview, ProductVariation


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "category", "subcategory", "stock"]
    readonly_fields = ["ordered_count"]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery)
admin.site.register(ProductReview)
admin.site.register(ProductVariation)