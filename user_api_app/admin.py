from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "age",
        "country",
        "is_staff",
        "is_active",
        "receive_mails",
    )
    list_filter = (
        "email",
        "age",
        "country",
        "is_staff",
        "is_active",
        "receive_mails",
    )
    fieldsets = (
        (None, {"fields": ("email", "password", "age", "country", "receive_mails")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "age",
                    "receive_mails",
                    "country",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
