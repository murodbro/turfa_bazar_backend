from django.contrib import admin

from .models import Account


class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ("id", "email", "first_name", "phone", "is_staff", "is_active", "is_superuser")
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active", "groups", "user_permissions"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Account, AccountAdmin)
