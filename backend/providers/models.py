# backend/providers/models.py
import uuid

from django.db import models


class Provider(models.Model):
    SERVICE_TYPES = [
        ("AMBULANCE", "Ambulance Service"),
        ("FIRE_TRUCK", "Fire Truck"),
        ("POLICE_CAR", "Police Vehicle"),
        ("TOW_TRUCK", "Tow Truck"),
        ("PLUMBER", "Plumber"),
        ("ELECTRICIAN", "Electrician"),
        ("LOCKSMITH", "Locksmith"),
        ("GENERAL", "General Emergency"),
    ]

    STATUS_CHOICES = [
        ("OFFLINE", "Offline"),
        ("AVAILABLE", "Available"),
        ("ON_DUTY", "On Duty"),
        ("IN_EMERGENCY", "In Emergency"),
        ("BREAK", "On Break"),
    ]

    id = models.UUIDField(  # noqa: A003
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="provider_profile"
    )

    # Service information
    service_types = models.JSONField(default=list)  # Changed from ArrayField
    certification_level = models.CharField(max_length=50, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Current state
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OFFLINE")

    # Location - using simple Float fields instead of PointField for now
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Fix: Use string reference instead of direct model reference
    current_emergency_id = models.UUIDField(
        null=True, blank=True
    )  # Store ID instead of ForeignKey

    # Vehicle information
    vehicle_type = models.CharField(max_length=50, blank=True)
    vehicle_number = models.CharField(max_length=50, blank=True)
    vehicle_capacity = models.IntegerField(default=1)

    # Performance metrics
    total_emergencies = models.IntegerField(default=0)
    completed_emergencies = models.IntegerField(default=0)
    avg_response_time = models.DurationField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    rating_count = models.IntegerField(default=0)

    # Availability
    schedule = models.JSONField(default=dict, blank=True)  # Changed to JSONField
    last_ping = models.DateTimeField(null=True, blank=True)
    max_distance = models.IntegerField(default=50000)  # Max service distance in meters

    # Financial
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = "providers"

    def __str__(self):
        return f"{self.user.get_full_name()}"

    @property
    def current_emergency(self):
        """Get the current emergency instance"""
        if self.current_emergency_id:
            from emergencies.models import Emergency

            try:
                return Emergency.objects.get(id=self.current_emergency_id)
            except Emergency.DoesNotExist:
                return None
        return None
