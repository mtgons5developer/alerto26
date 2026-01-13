# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from providers.admin import ProviderInline
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [ProviderInline]

    # What to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 
                    'phone', 'is_staff', 'is_superuser', 'is_active', 'is_online')
    
    # Filter options on the right
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'is_online')
    
    # Search fields
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    
    # Fieldsets for detail view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Alerto24 Info', {'fields': ('user_type', 'emergency_contacts', 'medical_info', 
                                     'blood_type', 'last_known_location', 'is_online',
                                     'notification_preferences')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields for creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'user_type', 'password1', 'password2'),
        }),
    )
    
    # Ordering
    ordering = ('-date_joined',)
    
    # Make certain fields read-only
    readonly_fields = ('last_login', 'date_joined')