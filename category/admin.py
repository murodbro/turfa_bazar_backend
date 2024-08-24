from django.contrib import admin

from .models import ProductCategory, SubProductCategory


class ProductCategoryInlineAdmin(admin.TabularInline):
    model = SubProductCategory
    prepopulated_fields = {"slug": ("name",)}
    extra = 1

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductCategoryInlineAdmin]

class SubProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(SubProductCategory, SubProductCategoryAdmin)