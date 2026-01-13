from django.contrib import admin
from .models import Emergency

@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "code",
        "emergency_type",
        "priority",
        "status",
        "latitude",
        "longitude",
        "address",
        "city",
        "is_anonymous",
        "created_at",
        "provider",
    )
    list_filter = ("status", "emergency_type", "priority")
    search_fields = ("code", "address", "city", "user__email")
