# backend/users/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User model extending AbstractUser"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(max_length=20, default='CITIZEN')
    
    # Use django.db.models.JSONField instead of django.contrib.postgres.fields.JSONField
    emergency_contacts = models.JSONField(default=list, blank=True)
    medical_info = models.JSONField(default=dict, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    
    # Location tracking
    last_known_location = models.CharField(max_length=100, blank=True)
    is_online = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)
    
    # Notification preferences
    push_token = models.TextField(blank=True)
    notification_preferences = models.JSONField(default=dict, blank=True)
    
    # Fix: Add custom related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  # Custom related_name
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # Custom related_name
        related_query_name='user',
    )
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.email} ({self.user_type})"