from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import Car, Rental, CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        ("Additional Info", {"fields": ("phone_number", "address")}),
    )
    add_fieldsets = (
        *UserAdmin.fieldsets,
        ("Additional Info", {"fields": ("phone_number", "address")}),
    )

    model = CustomUser
    list_display = [
        "username",
        "email",
        "phone_number",
        "address",
        "is_staff",
        "is_active",
    ]
    search_fields = ("username",)
    ordering = ("username",)


class CustomCarAdmin(admin.ModelAdmin):
    model = Car
    list_display: list[str] = [
        "name",
        "brand",
        "model",
        "price",
        "available",
        "image",
    ]
    ordering = (
        "name",
        "brand",
        "model",
        "price",
        "available",
    )


class CustomRentalAdmin(admin.ModelAdmin):
    model = Rental
    list_display: list[str] = [
        "car",
        "user",
        "rental_date",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Car, CustomCarAdmin)
admin.site.register(Rental, CustomRentalAdmin)
