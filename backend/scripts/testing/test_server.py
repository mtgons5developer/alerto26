# test_server.py
import requests
import sys

def test_server():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Django server...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get(base_url + "/")
        print(f"✅ Server is running (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running! Start it with: python manage.py runserver")
        return False
    
    # Test 2: Check admin (should exist by default)
    try:
        response = requests.get(base_url + "/admin/")
        print(f"✅ Admin page exists (Status: {response.status_code})")
    except:
        print("⚠️  Admin page not accessible")
    
    # Test 3: Check GraphQL endpoint
    try:
        response = requests.get(base_url + "/graphql/")  # Note trailing slash
        print(f"GraphQL GET: Status {response.status_code}")
        
        if response.status_code == 200:
            print("✅ GraphQL endpoint is accessible!")
            return True
        elif response.status_code == 404:
            print("❌ GraphQL endpoint returns 404 - Not configured in urls.py")
            return False
    except Exception as e:
        print(f"❌ Error accessing GraphQL: {e}")
        return False

if __name__ == "__main__":
    if test_server():
        print("\n🎉 Server is ready for GraphQL testing!")
    else:
        print("\n🔧 You need to fix the URL configuration first.")