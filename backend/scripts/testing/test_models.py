# scripts/testing/test_models.py
import os
import django
import sys

# Setup Django
sys.path.append('/Users/ernestoh.almeda.jr/alerto24/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from emergencies.models import Emergency
from providers.models import Provider
from datetime import datetime

def test_user_model():
    """Test User model creation"""
    User = get_user_model()
    
    # Create test user
    user = User.objects.create_user(
        username='testuser1',
        email='test1@alerto24.app',
        password='password123',
        phone='+15550000001',
        user_type='CITIZEN'
    )
    
    print(f"✅ Created User: {user.email} (ID: {user.id})")
    return user

def test_emergency_model():
    """Test Emergency model creation"""
    User = get_user_model()
    user = User.objects.first() or test_user_model()
    
    emergency = Emergency.objects.create(
        user=user,
        emergency_type='MEDICAL',
        latitude=40.7128,
        longitude=-74.0060,
        address='Times Square, NYC',
        description='Test medical emergency'
    )
    
    print(f"✅ Created Emergency: {emergency.code}")
    print(f"   Type: {emergency.emergency_type}")
    print(f"   Location: {emergency.latitude}, {emergency.longitude}")
    
    return emergency

def test_provider_model():
    """Test Provider model creation"""
    User = get_user_model()
    
    # Create provider user
    provider_user = User.objects.create_user(
        username='provider1',
        email='provider1@alerto24.app',
        password='password123',
        phone='+15550000002',
        user_type='PROVIDER'
    )
    
    provider = Provider.objects.create(
        user=provider_user,
        service_types=['AMBULANCE', 'MEDICAL'],
        status='AVAILABLE',
        latitude=40.7589,
        longitude=-73.9851,
        rating=4.5
    )
    
    print(f"✅ Created Provider: {provider.user.email}")
    print(f"   Services: {provider.service_types}")
    print(f"   Status: {provider.status}")
    
    return provider

def test_relationships():
    """Test model relationships"""
    User = get_user_model()
    
    # Create user with emergencies
    user = User.objects.create_user(
        username='citizen1',
        email='citizen1@alerto24.app',
        password='password123',
        phone='+15550000003',
        user_type='CITIZEN'
    )
    
    # Create multiple emergencies
    emergencies = []
    for i in range(3):
        emergency = Emergency.objects.create(
            user=user,
            emergency_type=['MEDICAL', 'FIRE', 'POLICE'][i],
            latitude=40.7128 + (i * 0.01),
            longitude=-74.0060 + (i * 0.01),
            description=f"Test emergency {i+1}"
        )
        emergencies.append(emergency)
    
    print(f"✅ Created {len(emergencies)} emergencies for user {user.email}")
    print(f"   User has {user.emergencies.count()} emergencies")
    
    # Test provider assignment
    provider = Provider.objects.first() or test_provider_model()
    emergencies[0].provider = provider
    emergencies[0].save()
    
    print(f"✅ Assigned provider to emergency: {provider.user.email}")
    print(f"   Provider has {provider.assigned_emergencies.count()} assigned emergencies")

if __name__ == "__main__":
    print("🧪 Testing AlertO24 Models")
    print("=" * 40)
    
    try:
        test_user_model()
        test_emergency_model()
        test_provider_model()
        test_relationships()
        print("\n🎉 All model tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()