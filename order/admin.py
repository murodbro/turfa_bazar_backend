from django.contrib import admin
from .models import Order, OrderItems


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "buy_cash", "recive_by_deliver"]
    readonly_fields = ["order_code", "smtp_code"]

admin.site.register(Order, OrderAdmin)


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "order", "status", "sub_total"]

admin.site.register(OrderItems, OrderItemsAdmin)
