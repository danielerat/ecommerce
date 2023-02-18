from store.models import Product
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin, ProductImageInline
from tags.models import TaggedItem
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name","phone_number", "email")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name","last_name","username", "email","phone_number", "password1", "password2"),
            },
        ),
    )

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline,ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
