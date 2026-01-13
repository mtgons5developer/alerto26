from django.contrib import admin
from .models import Emergency


@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
    )
