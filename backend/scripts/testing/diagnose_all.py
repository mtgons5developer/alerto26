# diagnose_all.py
import os
import sys
import django
import requests

# Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print("=" * 70)
print("🔍 COMPREHENSIVE GRAPHQL DIAGNOSIS")
print("=" * 70)

try:
    django.setup()
    
    from django.conf import settings
    
    print("\n📋 1. DJANGO SETTINGS CHECK:")
    print("-" * 40)
    
    # Check INSTALLED_APPS
    if 'graphene_django' in settings.INSTALLED_APPS:
        print("✅ graphene_django in INSTALLED_APPS")
    else:
        print("❌ graphene_django NOT in INSTALLED_APPS")
    
    # Check GRAPHENE config
    if hasattr(settings, 'GRAPHENE'):
        print(f"✅ GRAPHENE config: {settings.GRAPHENE}")
    else:
        print("❌ No GRAPHENE configuration")
    
    # Check DEBUG mode
    print(f"📊 DEBUG mode: {settings.DEBUG}")
    
    print("\n📋 2. DATABASE CHECK:")
    print("-" * 40)
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print(f"✅ Database connected: {db_version[0]}")
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    print("\n📋 3. SCHEMA VALIDATION:")
    print("-" * 40)
    try:
        from config.schema import schema
        
        # Test schema execution
        test_query = """
        {
            __schema {
                types {
                    name
                }
            }
        }
        """
        result = schema.execute(test_query)
        
        if result.errors:
            print(f"❌ Schema has errors: {result.errors}")
        else:
            print("✅ Schema validates successfully")
            
            # List available types
            types = result.data['__schema']['types']
            query_types = [t['name'] for t in types if t['name'].startswith('Query') or t['name'] in ['EmergencyType', 'ProviderType']]
            print(f"📊 Found types: {', '.join(query_types[:10])}...")
            
    except Exception as e:
        print(f"❌ Schema error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n📋 4. GRAPHQL ENDPOINT TEST:")
    print("-" * 40)
    
    # Test with requests
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        health_resp = requests.get(f"{base_url}/health/", timeout=2)
        print(f"✅ Health endpoint: {health_resp.status_code} - {health_resp.text}")
    except:
        print("⚠️  Health endpoint not reachable")
    
    # Test GraphQL endpoint
    try:
        # Test GET (should show GraphiQL)
        get_resp = requests.get(f"{base_url}/graphql/", timeout=2)
        print(f"\n📡 GraphQL GET: {get_resp.status_code}")
        
        if get_resp.status_code == 200:
            if 'text/html' in get_resp.headers.get('Content-Type', ''):
                print("✅ GraphiQL interface detected")
            else:
                print(f"📄 Response type: {get_resp.headers.get('Content-Type')}")
        elif get_resp.status_code == 400:
            print("⚠️  GET returns 400 (might need POST for queries)")
        
        # Test POST with query
        post_data = {
            'query': '''
            query {
                __typename
            }
            '''
        }
        post_resp = requests.post(
            f"{base_url}/graphql/",
            json=post_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        print(f"\n📡 GraphQL POST: {post_resp.status_code}")
        
        if post_resp.status_code == 200:
            data = post_resp.json()
            if 'errors' in data:
                print(f"❌ GraphQL errors: {data['errors']}")
            else:
                print(f"✅ GraphQL response: {data}")
        else:
            print(f"📄 Response: {post_resp.text[:200]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        print("💡 Run: python manage.py runserver")
    except Exception as e:
        print(f"❌ Request error: {e}")
    
    print("\n📋 5. QUERY SPECIFIC TESTS:")
    print("-" * 40)
    
    # Test actual queries from your schema
    test_queries = [
        {
            'name': 'Simple type query',
            'query': '{ __typename }'
        },
        {
            'name': 'List emergencies',
            'query': '{ emergencies { id emergencyType } }'
        },
        {
            'name': 'List providers', 
            'query': '{ providers { id name } }'
        }
    ]
    
    for test in test_queries:
        try:
            response = requests.post(
                f"{base_url}/graphql/",
                json={'query': test['query']},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'errors' in data:
                    print(f"❌ {test['name']}: {data['errors'][0]['message']}")
                else:
                    print(f"✅ {test['name']}: Success")
            else:
                print(f"❌ {test['name']}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {test['name']}: {e}")
    
    print("\n" + "=" * 70)
    print("🚀 QUICK FIXES IF NEEDED:")
    print("=" * 70)
    
    # Generate recommended fixes
    print("\n1. Ensure graphene_django is in INSTALLED_APPS:")
    print('   INSTALLED_APPS = [')
    print("       ...")
    print("       'graphene_django',")
    print("       ...")
    print('   ]')
    
    print("\n2. Add GRAPHENE configuration to settings.py:")
    print('   GRAPHENE = {')
    print("       'SCHEMA': 'config.schema.schema',")
    print("       'MIDDLEWARE': [")
    print("           'graphql_jwt.middleware.JSONWebTokenMiddleware',")
    print("       ],")
    print('   }')
    
    print("\n3. Add JWT configuration (if using authentication):")
    print('   AUTHENTICATION_BACKENDS = [')
    print("       'graphql_jwt.backends.JSONWebTokenBackend',")
    print("       'django.contrib.auth.backends.ModelBackend',")
    print('   ]')
    
    print("\n4. Run migrations for your models:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    
    print("\n5. Test with curl:")
    print('   curl -X POST http://localhost:8000/graphql/ \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"query": "{ emergencies { id } }"}\'')
    
except Exception as e:
    print(f"\n❌ Diagnosis failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("🎯 NEXT STEPS:")
print("=" * 70)
print("1. Run this diagnosis: python diagnose_all.py")
print("2. Check the output above")
print("3. Share any error messages")
print("4. Test in browser: http://localhost:8000/graphql/")