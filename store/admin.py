from django.contrib import admin

from .models import Product, VariationType, VariationValue, ProductVariation, ProductReview, ProductGallery


class ProductGalleryInlineAdmin(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductVariationsInlineAdmin(admin.TabularInline):
    model = ProductVariation
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "category", "subcategory"]
    readonly_fields = ["ordered_count"]
    inlines = [ProductGalleryInlineAdmin, ProductVariationsInlineAdmin]


class ProductVariationTypeInlineAdmin(admin.TabularInline):
    model = VariationValue
    extra = 1


class ProductVariationTypeAdmin(admin.ModelAdmin):
    inlines = [ProductVariationTypeInlineAdmin]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery)
admin.site.register(ProductReview)
admin.site.register(VariationType, ProductVariationTypeAdmin)
admin.site.register(VariationValue)
admin.site.register(ProductVariation)
