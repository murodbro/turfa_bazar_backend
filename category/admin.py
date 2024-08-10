from django.contrib import admin

from .models import ProductCategory, SubProductCategory


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ("name",)}

class SubProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(SubProductCategory, SubProductCategoryAdmin)