# backend/providers/models.py
import uuid
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import ArrayField, JSONField

class Provider(models.Model):
    SERVICE_TYPES = [
        ('AMBULANCE', 'Ambulance Service'),
        ('FIRE_TRUCK', 'Fire Truck'),
        ('POLICE_CAR', 'Police Vehicle'),
        ('TOW_TRUCK', 'Tow Truck'),
        ('PLUMBER', 'Plumber'),
        ('ELECTRICIAN', 'Electrician'),
        ('LOCKSMITH', 'Locksmith'),
        ('GENERAL', 'General Emergency'),
    ]
    
    STATUS_CHOICES = [
        ('OFFLINE', 'Offline'),
        ('AVAILABLE', 'Available'),
        ('ON_DUTY', 'On Duty'),
        ('IN_EMERGENCY', 'In Emergency'),
        ('BREAK', 'On Break'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='provider_profile')
    
    # Service information
    service_types = ArrayField(models.CharField(max_length=50, choices=SERVICE_TYPES))
    certification_level = models.CharField(max_length=50, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Current state
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OFFLINE')
    current_location = gis_models.PointField(geography=True, null=True, blank=True)
    current_emergency = models.ForeignKey('emergencies.Emergency', on_delete=models.SET_NULL, null=True, blank=True, related_name='active_provider')
    
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
    schedule = JSONField(default=dict, blank=True)  # Weekly schedule
    last_ping = models.DateTimeField(null=True, blank=True)
    max_distance = models.IntegerField(default=50000)  # Max service distance in meters
    
    # Financial
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = 'providers'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {', '.join(self.service_types)}"