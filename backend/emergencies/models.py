# backend/emergencies/models.py
import uuid
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import ArrayField, JSONField

class Emergency(models.Model):
    EMERGENCY_TYPES = [
        ('MEDICAL', 'Medical Emergency'),
        ('FIRE', 'Fire'),
        ('POLICE', 'Police'),
        ('CAR_ACCIDENT', 'Car Accident'),
        ('NATURAL_DISASTER', 'Natural Disaster'),
        ('UTILITY', 'Utility Failure'),
        ('OTHER', 'Other'),
    ]
    
    PRIORITY_LEVELS = [
        ('RED', 'Critical - Immediate response'),
        ('ORANGE', 'High - Urgent'),
        ('YELLOW', 'Medium - Prompt'),
        ('GREEN', 'Low - Routine'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('DISPATCHED', 'Dispatched'),
        ('EN_ROUTE', 'En Route'),
        ('ON_SITE', 'On Site'),
        ('RESOLVED', 'Resolved'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=20, unique=True)  # EMT-2024-001
    
    # Relationships
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='emergencies')
    provider = models.ForeignKey('providers.Provider', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_emergencies')
    dispatcher = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='dispatched_emergencies')
    
    # Emergency details
    emergency_type = models.CharField(max_length=50, choices=EMERGENCY_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='YELLOW')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Location
    location = gis_models.PointField(geography=True)
    user_location = gis_models.PointField(geography=True, null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Medical-specific (if applicable)
    symptoms = ArrayField(models.CharField(max_length=100), default=list, blank=True)
    patient_info = JSONField(default=dict, blank=True)
    
    # Metadata
    description = models.TextField(blank=True)
    attachments = ArrayField(models.URLField(), default=list, blank=True)
    is_anonymous = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    arrived_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Performance metrics
    response_time = models.DurationField(null=True, blank=True)
    resolution_time = models.DurationField(null=True, blank=True)
    
    class Meta:
        db_table = 'emergencies'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['provider', 'status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.code:
            # Generate unique code: EMT-YYYY-XXXX
            from django.utils import timezone
            year = timezone.now().strftime('%Y')
            last_emergency = Emergency.objects.filter(code__startswith=f'EMT-{year}-').order_by('code').last()
            if last_emergency:
                last_num = int(last_emergency.code.split('-')[-1])
                self.code = f'EMT-{year}-{last_num + 1:04d}'
            else:
                self.code = f'EMT-{year}-0001'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.code} - {self.get_emergency_type_display()}"