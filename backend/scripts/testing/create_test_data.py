# create_alerto_test_data.py
import json
import os
import random
import sys
from datetime import datetime, timedelta
from decimal import Decimal

import django
from django.db.models import Count

from emergencies.models import Emergency
from providers.models import Provider

# Import your models
from users.models import User

# Setup Django
sys.path.insert(0, os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

print("🧪 Creating Test Data for Alerto24")
print("=" * 60)
print("✅ Models imported successfully")

# Clear existing data (optional - comment out if you want to keep existing data)
print("\n🗑️  Clearing existing data...")
# Emergency.objects.all().delete()
# Provider.objects.all().delete()
# User.objects.filter(is_superuser=False).delete()  # Keep admin users

# Create regular citizen users
print("\n👥 Creating citizen users...")
citizens = []

user_types = [
    "CITIZEN",
    "CITIZEN",
    "CITIZEN",
    "FIRST_RESPONDER",
    "ADMIN",
]  # Mostly citizens
# Users
for i in range(1000):
    try:
        user = User.objects.create_user(
            username=f"citizen{i + 1}",
            email=f"citizen{i + 1}@example.com",
            password="password123",
            first_name=f"Citizen{i + 1}",
            last_name="User",
            phone=f"+63{9000000000 + i}",  # Unique phone numbers
            user_type=random.choice(user_types),
            emergency_contacts=json.dumps(
                [
                    {
                        "name": "Emergency Contact 1",
                        "phone": "+639001112233",
                        "relationship": "Family",
                    },
                    {
                        "name": "Emergency Contact 2",
                        "phone": "+639004445566",
                        "relationship": "Friend",
                    },
                ]
            ),
            medical_info=json.dumps(
                {
                    "allergies": (
                        ["Penicillin", "Peanuts"]
                        if random.choice([True, False])
                        else []
                    ),
                    "conditions": (
                        ["Asthma", "Hypertension"]
                        if random.choice([True, False])
                        else []
                    ),
                    "medications": (
                        ["Metformin", "Lisinopril"]
                        if random.choice([True, False])
                        else []
                    ),
                }
            ),
            blood_type=random.choice(
                ["O+", "A+", "B+", "AB+", "O-", "A-", "B-", "AB-", ""]
            ),
            last_known_location=f"{14.5995 + random.uniform(-0.1, 0.1)},{120.9842 + random.uniform(-0.1, 0.1)}",
            is_online=random.choice([True, False]),
            notification_preferences=json.dumps(
                {
                    "emergency_alerts": True,
                    "provider_updates": True,
                    "promotional": False,
                }
            ),
        )
        citizens.append(user)
        # print(f"  ✅ {user.username} ({user.user_type})")
    except Exception as e:
        print(f"  ⚠️  Error creating citizen{i + 1}: {str(e)[:100]}")

print(f"📊 Created {len(citizens)} citizen users")

# Create provider users
print("\n👨‍⚕️ Creating provider users...")
provider_users = []
# Providers
for i in range(500):
    try:
        user = User.objects.create_user(
            username=f"provider_user{i + 1}",
            email=f"provider{i + 1}@example.com",
            password="password123",
            first_name=f"Provider{i + 1}",
            last_name="Responder",
            phone=f"+63{9100000000 + i}",  # Different range for providers
            user_type="PROVIDER",  # Provider user type
            emergency_contacts=json.dumps([]),
            medical_info=json.dumps({}),
            is_online=True,  # Providers are usually online
            notification_preferences=json.dumps(
                {
                    "emergency_alerts": True,
                    "dispatch_requests": True,
                    "system_updates": True,
                }
            ),
        )
        provider_users.append(user)
        # print(f"  ✅ {user.username} (PROVIDER)")
    except Exception as e:
        print(f"  ⚠️  Error creating provider user{i + 1}: {str(e)[:100]}")

# Create admin user if not exists
if not User.objects.filter(username="admin").exists():
    try:
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
            first_name="Admin",
            last_name="User",
            phone="+639000000001",
            user_type="ADMIN",
        )
        # print(f"  ✅ {admin.username} (ADMIN superuser)")
    except Exception as e:
        print(f"  ⚠️  Error creating admin: {str(e)[:100]}")

print(f"\n📊 Total users: {User.objects.count()}")

# Create providers (linked to provider users)
print("\n🏥 Creating provider profiles...")
providers = []

service_type_combinations = [
    ["AMBULANCE"],
    ["FIRE_TRUCK"],
    ["POLICE_CAR"],
    ["AMBULANCE", "TOW_TRUCK"],
    ["POLICE_CAR", "AMBULANCE"],
    ["GENERAL"],
    ["ELECTRICIAN", "PLUMBER"],
    ["LOCKSMITH"],
]

for i, user in enumerate(provider_users[:8]):  # Use first 8 provider users
    try:
        provider = Provider.objects.create(
            user=user,
            service_types=json.dumps(
                service_type_combinations[i % len(service_type_combinations)]
            ),
            certification_level=random.choice(
                ["Basic", "Advanced", "Expert", "Certified"]
            ),
            license_number=f"PH-LIC-{random.randint(10000, 99999)}",
            is_verified=random.choice([True, True, False]),  # Mostly verified
            verification_date=datetime.now() - timedelta(days=random.randint(30, 365)),
            is_active=True,
            status=random.choice(["AVAILABLE", "ON_DUTY", "BREAK"]),
            latitude=14.5995 + random.uniform(-0.15, 0.15),
            longitude=120.9842 + random.uniform(-0.15, 0.15),
            vehicle_type=random.choice(
                ["Ambulance", "Fire Truck", "Police Car", "SUV", "Van"]
            ),
            vehicle_number=f"{random.choice(['NCR', 'MM', 'PH'])}-{random.randint(1000, 9999)}",
            vehicle_capacity=random.randint(1, 8),
            total_emergencies=random.randint(5, 100),
            completed_emergencies=random.randint(5, 95),
            avg_response_time=timedelta(minutes=random.randint(8, 25)),
            rating=Decimal(str(round(random.uniform(3.5, 5.0), 2))),
            rating_count=random.randint(5, 150),
            schedule=json.dumps(
                {
                    "monday": {"start": "08:00", "end": "20:00"},
                    "tuesday": {"start": "08:00", "end": "20:00"},
                    "wednesday": {"start": "08:00", "end": "20:00"},
                    "thursday": {"start": "08:00", "end": "20:00"},
                    "friday": {"start": "08:00", "end": "20:00"},
                    "saturday": {"start": "10:00", "end": "18:00"},
                    "sunday": {"start": "10:00", "end": "16:00"},
                }
            ),
            last_ping=datetime.now() - timedelta(minutes=random.randint(1, 30)),
            max_distance=random.choice([10000, 25000, 50000]),  # 10km, 25km, 50km
            hourly_rate=Decimal(str(round(random.uniform(500, 1500), 2))),
            service_fee=Decimal(str(round(random.uniform(200, 800), 2))),
        )
        providers.append(provider)
        # print(f"  ✅ {user.first_name}: {provider.service_types} ({provider.status})")
    except Exception as e:
        print(f"  ❌ Error creating provider for {user.username}: {str(e)[:100]}")

print(f"📊 Created {len(providers)} provider profiles")

# Create emergencies
print("\n🚨 Creating emergency cases...")

emergency_types = [
    "medical",
    "fire",
    "police",
    "accident",
    "natural_disaster",
    "hazard",
]
philippine_cities = [
    "Manila",
    "Quezon City",
    "Makati",
    "Taguig",
    "Pasig",
    "Mandaluyong",
    "San Juan",
    "Paranaque",
    "Las Pinas",
    "Muntinlupa",
]

symptoms_examples = {
    "medical": ["Chest pain", "Difficulty breathing", "Unconscious", "Severe bleeding"],
    "fire": ["Smoke visible", "Open flames", "Electrical sparks", "Burning smell"],
    "police": ["Assault in progress", "Burglary", "Disturbance", "Suspicious activity"],
    "accident": [
        "Vehicle collision",
        "Multiple injuries",
        "Road blocked",
        "Trapped person",
    ],
}

emergencies_created = 0
# emergency
for i in range(1001):
    try:
        # Random citizen reporter (or anonymous)
        reporter = (
            random.choice(citizens) if random.choice([True, True, False]) else None
        )  # 2/3 chance

        # Random provider assignment (or none)
        assigned_provider = (
            random.choice(providers)
            if providers and random.choice([True, False])
            else None
        )

        emergency_type = random.choice(emergency_types)

        # Create emergency
        emergency = Emergency.objects.create(
            code=f"ALERT-2025-{random.randint(1000, 9999)}",
            user=reporter,
            provider=assigned_provider,
            emergency_type=emergency_type,
            priority=random.choice(["low", "medium", "high", "critical"]),
            status=random.choice(["pending", "dispatched", "arrived", "resolved"]),
            latitude=14.5995 + random.uniform(-0.2, 0.2),
            longitude=120.9842 + random.uniform(-0.2, 0.2),
            address=f"{random.randint(1, 999)} {random.choice(['EDSA', 'C5', 'Roxas Blvd', 'Ayala Ave', 'Shaw Blvd'])}",
            city=random.choice(philippine_cities),
            symptoms=json.dumps(
                random.sample(
                    symptoms_examples.get(emergency_type, ["Emergency reported"]),
                    random.randint(1, 3),
                )
            ),
            patient_info=(
                json.dumps(
                    {
                        "name": f"{random.choice(['Juan', 'Maria', 'Pedro', 'Ana'])} {random.choice(['Dela Cruz', 'Santos', 'Reyes', 'Lopez'])}",
                        "age": random.randint(18, 75),
                        "gender": random.choice(["male", "female"]),
                        "blood_type": random.choice(["O+", "A+", "B+", "AB+"]),
                    }
                )
                if emergency_type in ["medical", "accident"]
                else json.dumps({})
            ),
            description=f"{emergency_type.capitalize()} emergency reported at {random.choice(['residential area', 'commercial establishment', 'public road', 'park'])}",
            attachments=json.dumps(
                [f"photo_{j + 1}.jpg" for j in range(random.randint(0, 2))]
            ),
            is_anonymous=reporter is None,
            created_at=datetime.now()
            - timedelta(hours=random.randint(0, 168)),  # Up to 7 days ago
        )

        # Update timestamps based on status
        if emergency.status in ["dispatched", "arrived", "resolved"]:
            emergency.dispatched_at = emergency.created_at + timedelta(
                minutes=random.randint(2, 15)
            )

        if emergency.status in ["arrived", "resolved"]:
            emergency.arrived_at = emergency.dispatched_at + timedelta(
                minutes=random.randint(5, 30)
            )

        if emergency.status == "resolved":
            emergency.resolved_at = emergency.arrived_at + timedelta(
                minutes=random.randint(20, 120)
            )

        emergency.save()

        # Update provider if assigned
        if assigned_provider and emergency.status in ["dispatched", "arrived"]:
            assigned_provider.current_emergency_id = emergency.id
            assigned_provider.status = "IN_EMERGENCY"
            assigned_provider.save()

        emergencies_created += 1
        # print(f"  ✅ {emergency.code}: {emergency_type} in {emergency.city} ({emergency.status})")

    except Exception as e:
        print(f"  ⚠️  Error creating emergency {i + 1}: {str(e)[:100]}")

print(f"\n📊 Created {emergencies_created} emergencies")

# Display comprehensive summary
print("\n" + "=" * 60)
print("📈 ALERTO24 DATA SUMMARY")
print("=" * 60)

print("\n👥 USER STATISTICS:")
print(f"  Total users: {User.objects.count()}")
for user_type in ["CITIZEN", "PROVIDER", "FIRST_RESPONDER", "ADMIN"]:
    count = User.objects.filter(user_type=user_type).count()
    if count > 0:
        print(f"  {user_type}: {count}")

print("\n🏥 PROVIDER STATISTICS:")
print(f"  Total providers: {Provider.objects.count()}")
print(f"  Verified providers: {Provider.objects.filter(is_verified=True).count()}")
print(f"  Active providers: {Provider.objects.filter(is_active=True).count()}")
for status in ["AVAILABLE", "ON_DUTY", "IN_EMERGENCY", "BREAK", "OFFLINE"]:
    count = Provider.objects.filter(status=status).count()
    if count > 0:
        print(f"  {status}: {count}")

print("\n🚨 EMERGENCY STATISTICS:")
print(f"  Total emergencies: {Emergency.objects.count()}")
print(f"  Anonymous reports: {Emergency.objects.filter(is_anonymous=True).count()}")
print(f"  User reports: {Emergency.objects.filter(is_anonymous=False).count()}")

print("\n📊 EMERGENCY TYPES:")
for etype in emergency_types:
    count = Emergency.objects.filter(emergency_type=etype).count()
    if count > 0:
        print(f"  {etype}: {count}")

print("\n📊 EMERGENCY STATUS:")
for status in ["pending", "dispatched", "arrived", "resolved"]:
    count = Emergency.objects.filter(status=status).count()
    print(f"  {status}: {count}")

print("\n📊 EMERGENCY PRIORITY:")
for priority in ["low", "medium", "high", "critical"]:
    count = Emergency.objects.filter(priority=priority).count()
    if count > 0:
        print(f"  {priority}: {count}")

print("\n🏙️  TOP CITIES WITH EMERGENCIES:")

for item in (
    Emergency.objects.values("city").annotate(count=Count("id")).order_by("-count")[:5]
):
    print(f"  {item['city']}: {item['count']}")

print("\n" + "=" * 60)
print("🚀 GRAPHQL API READY FOR TESTING")
print("=" * 60)

# print('''
# 🌐 Open in browser: http://localhost:8000/graphql/

# 📋 Sample GraphQL Queries:

# 1. Get all emergencies:
# {
#   emergencies {
#     id
#     code
#     emergencyType
#     priority
#     status
#     city
#     latitude
#     longitude
#     isAnonymous
#     createdAt
#   }
# }

# 2. Get all providers:
# {
#   providers {
#     id
#     user {
#       firstName
#       lastName
#       email
#       phone
#     }
#     serviceTypes
#     status
#     latitude
#     longitude
#     rating
#     totalEmergencies
#     isVerified
#   }
# }

# 3. Get active emergencies:
# {
#   emergencies(status: "pending") {
#     code
#     emergencyType
#     city
#     description
#     createdAt
#   }
# }

# 4. Get available providers:
# {
#   providers(status: "AVAILABLE") {
#     user {
#       firstName
#       lastName
#     }
#     serviceTypes
#     vehicleType
#     vehicleCapacity
#     rating
#     maxDistance
#   }
# }

# 5. Get emergency statistics:
# {
#   emergencies {
#     emergencyType
#     status
#     priority
#     city
#   }
# }

# 6. Test mutation (create emergency):
# mutation {
#   createEmergency(
#     emergencyType: "medical"
#     latitude: 14.5995
#     longitude: 120.9842
#   ) {
#     emergency {
#       id
#       code
#       emergencyType
#       latitude
#       longitude
#       createdAt
#     }
#   }
# }
# ''')

# print("\n💻 Test with curl:")
# print('''
# # Quick test - count data:
# curl -X POST http://localhost:8000/graphql/ \\
#   -H "Content-Type: application/json" \\
#   -d '{"query": "{ emergencies { id } providers { id } users { id } }"}'

# # Get emergencies:
# curl -X POST http://localhost:8000/graphql/ \\
#   -H "Content-Type: application/json" \\
#   -d '{"query": "{ emergencies { code emergencyType priority status city } }"}'

# # Get providers:
# curl -X POST http://localhost:8000/graphql/ \\
#   -H "Content-Type: application/json" \\
#   -d '{"query": "{ providers { user { firstName lastName } serviceTypes status rating } }"}'
# ''')

print("\n✅ Test data creation complete!")
print("🔑 Admin login: username='admin', password='admin123'")
print("🔑 Citizen login: username='citizen1', password='password123'")
print("🔑 Provider login: username='provider_user1', password='password123'")
