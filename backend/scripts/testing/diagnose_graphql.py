import os
import sys
import django
import requests
from pathlib import Path

# Get the project root (where manage.py is)
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print("=" * 70)
print("🔍 GRAPHQL & DJANGO DIAGNOSIS")
print("=" * 70)

try:
    django.setup()
    
    from django.conf import settings
    
    print("\n📋 1. DJANGO CONFIGURATION:")
    print("-" * 40)
    print(f"   Settings module: {settings.SETTINGS_MODULE}")
    print(f"   Debug mode: {settings.DEBUG}")
    print(f"   Installed apps count: {len(settings.INSTALLED_APPS)}")
    
    # Check graphene
    graphene_installed = 'graphene_django' in settings.INSTALLED_APPS
    print(f"   graphene_django installed: {'✅' if graphene_installed else '❌'}")
    
    if hasattr(settings, 'GRAPHENE'):
        print(f"   GRAPHENE config: ✅ {settings.GRAPHENE}")
    else:
        print("   GRAPHENE config: ❌ Not found")
    
    print("\n📋 2. DATABASE CONNECTION:")
    print("-" * 40)
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print(f"   ✅ Connected to: {db_version[0]}")
            
            # Check if tables exist
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name IN ('emergencies_emergency', 'providers_provider');
            """)
            tables = cursor.fetchall()
            print(f"   📊 Found tables: {[t[0] for t in tables]}")
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    print("\n📋 3. SCHEMA VALIDATION:")
    print("-" * 40)
    try:
        from config.schema import schema
        
        # Test a simple query
        result = schema.execute("{ __typename }")
        if result.errors:
            print(f"   ❌ Schema errors: {result.errors}")
        else:
            print(f"   ✅ Schema valid: {result.data}")
            
        # Test with actual models
        result2 = schema.execute("{ emergencies { id } }")
        if result2.errors:
            print(f"   ⚠️  Emergency query error: {result2.errors[0].message}")
        else:
            print(f"   ✅ Emergency query: {len(result2.data.get('emergencies', []))} items")
            
    except ImportError as e:
        print(f"   ❌ Cannot import schema: {e}")
    except Exception as e:
        print(f"   ❌ Schema validation error: {e}")
    
    print("\n📋 4. SERVER ENDPOINTS:")
    print("-" * 40)
    
    base_url = "http://localhost:8000"
    endpoints = [
        ("/health/", "GET"),
        ("/graphql/", "GET"),
        ("/graphql/", "POST"),
        ("/admin/", "GET"),
    ]
    
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                resp = requests.get(f"{base_url}{endpoint}", timeout=2)
            else:
                resp = requests.post(f"{base_url}{endpoint}", 
                                   json={"query": "{ __typename }"},
                                   headers={"Content-Type": "application/json"},
                                   timeout=2)
            
            status_icon = "✅" if resp.status_code in [200, 400] else "⚠️"
            print(f"   {status_icon} {method} {endpoint}: {resp.status_code}")
            
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {method} {endpoint}: Connection refused")
        except Exception as e:
            print(f"   ❌ {method} {endpoint}: {e}")
    
    print("\n📋 5. QUICK GRAPHQL TEST:")
    print("-" * 40)
    
    # Test GraphQL with curl-like request
    test_queries = [
        ("Introspection", "{ __schema { types { name } } }"),
        ("Emergency list", "{ emergencies { id emergencyType } }"),
        ("Provider list", "{ providers { id name } }"),
    ]
    
    for test_name, query in test_queries:
        try:
            resp = requests.post(
                f"{base_url}/graphql/",
                json={"query": query},
                headers={"Content-Type": "application/json"},
                timeout=3
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if "errors" in data:
                    error_msg = data["errors"][0]["message"][:50]
                    print(f"   ❌ {test_name}: {error_msg}...")
                else:
                    print(f"   ✅ {test_name}: Success")
            else:
                print(f"   ❌ {test_name}: HTTP {resp.status_code}")
                
        except Exception as e:
            print(f"   ❌ {test_name}: {e}")
    
    print("\n" + "=" * 70)
    print("💡 RECOMMENDED ACTIONS:")
    print("=" * 70)
    
    actions = []
    if not graphene_installed:
        actions.append("Add 'graphene_django' to INSTALLED_APPS in config/settings.py")
    
    if not hasattr(settings, 'GRAPHENE'):
        actions.append("Add GRAPHENE configuration to config/settings.py")
    
    if not actions:
        actions.append("Start server: python manage.py runserver")
        actions.append("Test in browser: http://localhost:8000/graphql/")
    
    for i, action in enumerate(actions, 1):
        print(f"{i}. {action}")
    
except Exception as e:
    print(f"\n❌ Setup failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("🚀 COMMANDS TO RUN:")
print("=" * 70)
print("1. Check Django: python manage.py check")
print("2. Run migrations: python manage.py migrate")
print("3. Start server: python manage.py runserver")
print("4. Test GraphQL: curl -X POST http://localhost:8000/graphql/ \\")
print('   -H "Content-Type: application/json" \\')
print('   -d \'{"query": "{ emergencies { id } }"}\'')
