# backend/users/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(max_length=20, choices=[
        ('CITIZEN', 'Citizen'),
        ('PROVIDER', 'Service Provider'),
        ('DISPATCHER', 'Dispatcher'),
        ('ADMIN', 'Administrator')
    ], default='CITIZEN')
    
    # Emergency information
    emergency_contacts = JSONField(default=list, blank=True)
    medical_info = JSONField(default=dict, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = ArrayField(models.CharField(max_length=100), default=list, blank=True)
    
    # Location tracking
    last_known_location = models.CharField(max_length=100, blank=True)
    is_online = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)
    
    # Notification preferences
    push_token = models.TextField(blank=True)
    notification_preferences = JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.email} ({self.user_type})"