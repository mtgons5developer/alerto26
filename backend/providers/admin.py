from django.contrib import admin
from .models import Provider


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "status",
        "is_verified",
        "is_active",
    )
    list_filter = ("status", "is_verified")
    search_fields = ("user__email", "user__first_name", "user__last_name")


class ProviderInline(admin.StackedInline):
    model = Provider
    can_delete = False