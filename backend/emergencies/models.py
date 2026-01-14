# backend/emergencies/models.py
import uuid

from django.db import models


class Emergency(models.Model):
    EMERGENCY_TYPES = [
        ("MEDICAL", "Medical Emergency"),
        ("FIRE", "Fire"),
        ("POLICE", "Police"),
        ("CAR_ACCIDENT", "Car Accident"),
        ("NATURAL_DISASTER", "Natural Disaster"),
        ("UTILITY", "Utility Failure"),
        ("OTHER", "Other"),
    ]

    PRIORITY_LEVELS = [
        ("RED", "Critical - Immediate response"),
        ("ORANGE", "High - Urgent"),
        ("YELLOW", "Medium - Prompt"),
        ("GREEN", "Low - Routine"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("DISPATCHED", "Dispatched"),
        ("EN_ROUTE", "En Route"),
        ("ON_SITE", "On Site"),
        ("RESOLVED", "Resolved"),
        ("CANCELLED", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=20, unique=True, blank=True)

    # Relationships
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="emergencies"
    )
    provider = models.ForeignKey(
        "providers.Provider",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_emergencies",
    )

    # Emergency details
    emergency_type = models.CharField(max_length=50, choices=EMERGENCY_TYPES)
    priority = models.CharField(
        max_length=20, choices=PRIORITY_LEVELS, default="YELLOW"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    # Location - using simple Float fields
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)

    # Medical-specific
    symptoms = models.JSONField(default=list, blank=True)
    patient_info = models.JSONField(default=dict, blank=True)

    # Metadata
    description = models.TextField(blank=True)
    attachments = models.JSONField(default=list, blank=True)
    is_anonymous = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    arrived_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "emergencies"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.code:
            from django.utils import timezone

            year = timezone.now().strftime("%Y")
            last_emergency = (
                Emergency.objects.filter(code__startswith=f"EMT-{year}-")
                .order_by("code")
                .last()
            )
            if last_emergency:
                last_num = int(last_emergency.code.split("-")[-1])
                self.code = f"EMT-{year}-{last_num + 1:04d}"
            else:
                self.code = f"EMT-{year}-0001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.get_emergency_type_display()}"
