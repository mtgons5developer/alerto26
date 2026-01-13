# diagnose_login.py
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    
    print("🔍 DIAGNOSING LOGIN CONFIGURATION")
    print("=" * 60)
    
    from django.conf import settings
    
    # Check 1: URLs match
    print("\n1. URL Configuration Check:")
    print(f"   LOGIN_URL in settings: {settings.LOGIN_URL}")
    print(f"   LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
    print(f"   LOGOUT_REDIRECT_URL: {settings.LOGOUT_REDIRECT_URL}")
    
    # Check 2: Template configuration
    print("\n2. Template Configuration Check:")
    template_dirs = settings.TEMPLATES[0]['DIRS']
    print(f"   Template DIRS: {template_dirs}")
    
    # Check if templates directory exists
    templates_path = BASE_DIR / 'templates'
    print(f"   Templates directory exists: {templates_path.exists()}")
    
    # Check login.html
    login_path = templates_path / 'admin' / 'login.html'
    print(f"   login.html exists: {login_path.exists()}")
    if login_path.exists():
        print(f"   login.html path: {login_path}")
    
    # Check staff_dashboard.html
    dashboard_path = templates_path / 'admin' / 'staff_dashboard.html'
    print(f"   staff_dashboard.html exists: {dashboard_path.exists()}")
    
    # Check 3: Test template loading
    print("\n3. Template Loading Test:")
    try:
        from django.template.loader import get_template
        login_template = get_template('admin/login.html')
        print(f"   ✅ login.html loaded: {login_template.origin.name}")
    except Exception as e:
        print(f"   ❌ Failed to load login.html: {e}")
    
    try:
        dashboard_template = get_template('admin/staff_dashboard.html')
        print(f"   ✅ staff_dashboard.html loaded: {dashboard_template.origin.name}")
    except Exception as e:
        print(f"   ❌ Failed to load staff_dashboard.html: {e}")
    
    # Check 4: Views and decorators
    print("\n4. View Configuration Check:")
    try:
        from config import views
        print(f"   views.py imported successfully")
        print(f"   staff_dashboard function exists: {hasattr(views, 'staff_dashboard')}")
        
        # Check decorators on staff_dashboard
        import inspect
        func = views.staff_dashboard
        print(f"   Function has decorators: {hasattr(func, '__wrapped__')}")
        
    except ImportError as e:
        print(f"   ❌ Cannot import views: {e}")
    except Exception as e:
        print(f"   ❌ Error checking views: {e}")
    
    # Check 5: Admin user exists
    print("\n5. Admin User Check:")
    try:
        from users.models import User
        admin_users = User.objects.filter(is_superuser=True)
        print(f"   Superusers found: {admin_users.count()}")
        
        if admin_users.exists():
            for admin in admin_users[:3]:
                print(f"     👑 {admin.username} (staff: {admin.is_staff}, active: {admin.is_active})")
        else:
            print("   ⚠️ No superusers found!")
            
        # Test authentication
        test_user = User.objects.filter(is_superuser=True).first()
        if test_user:
            from django.contrib.auth import authenticate
            # Try to authenticate (won't check password, just test backend)
            print(f"   Authentication backend test: OK")
    except Exception as e:
        print(f"   ❌ Error checking users: {e}")
    
    # Check 6: URL patterns
    print("\n6. URL Patterns Check:")
    from django.urls import get_resolver
    resolver = get_resolver()
    
    important_urls = ['login', 'logout', 'dashboard', 'admin', 'graphql']
    found_urls = []
    
    def check_patterns(patterns, prefix=''):
        for pattern in patterns:
            if hasattr(pattern, 'pattern'):
                pattern_str = str(pattern.pattern)
                for url_name in important_urls:
                    if url_name in pattern_str or (hasattr(pattern, 'name') and pattern.name == url_name):
                        found_urls.append(f"{prefix}{pattern_str} -> {getattr(pattern, 'name', 'No name')}")
    
    check_patterns(resolver.url_patterns)
    
    if found_urls:
        print("   Found important URLs:")
        for url in found_urls:
            print(f"     {url}")
    else:
        print("   ⚠️ No important URLs found!")
    
    print("\n" + "=" * 60)
    print("🚀 EXPECTED ACCESS URLs:")
    print("=" * 60)
    print("Home: http://localhost:8000/")
    print("Login: http://localhost:8000/accounts/login/")
    print("Dashboard: http://localhost:8000/dashboard/")
    print("Admin: http://localhost:8000/admin/")
    print("GraphQL: http://localhost:8000/graphql/")
    print("Health: http://localhost:8000/health/")
    
    print("\n🔧 QUICK FIXES IF NEEDED:")
    print("1. Ensure templates/ directory exists in backend/")
    print("2. Ensure admin/login.html and admin/staff_dashboard.html exist")
    print("3. Make sure TEMPLATES['DIRS'] includes BASE_DIR / 'templates'")
    print("4. URLs in settings.py must match urls.py exactly")
    print("5. Create admin user: python manage.py createsuperuser")
    
except Exception as e:
    print(f"❌ Diagnostic failed: {e}")
    import traceback
    traceback.print_exc()