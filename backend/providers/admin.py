from django.contrib import admin
from .models import Provider


class ProviderInline(admin.StackedInline):
    model = Provider
    can_delete = False
    extra = 0  # how many empty slots to show


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    # Fields to show in the list view
    list_display = (
        "user",
        "status",
        "is_verified",
        "is_active",
        "total_emergencies",
        "completed_emergencies",
        "rating",
        "vehicle_number",
        "hourly_rate",
        "service_fee",
    )

    # Filters on the right-hand sidebar
    list_filter = (
        "status",
        "is_verified",
        "is_active",
        "service_types",
    )

    # Fields searchable via the admin search bar
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "license_number",
        "vehicle_number",
    )

    # Organize fields on the add/edit form
    fieldsets = (
        ("User Info", {"fields": ("user",)}),
        ("Service Details", {
            "fields": (
                "service_types",
                "certification_level",
                "license_number",
                "is_verified",
                "verification_date",
                "is_active",
            )
        }),
        ("Current Status", {"fields": ("status", "latitude", "longitude", "current_emergency_id")}),
        ("Vehicle Info", {
            "fields": ("vehicle_type", "vehicle_number", "vehicle_capacity")
        }),
        ("Performance Metrics", {
            "fields": ("total_emergencies", "completed_emergencies", "avg_response_time", "rating", "rating_count")
        }),
        ("Availability & Schedule", {"fields": ("schedule", "last_ping", "max_distance")}),
        ("Financial", {"fields": ("hourly_rate", "service_fee")}),
    )
