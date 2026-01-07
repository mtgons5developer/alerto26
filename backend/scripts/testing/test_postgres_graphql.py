# test_graphql_debug.py
import requests
import json
import sys

def test_graphql_endpoint():
    """Test the GraphQL endpoint directly"""
    url = "http://localhost:8000/graphql"
    
    print("🔍 Testing GraphQL endpoint configuration...")
    
    # Test 1: Simple GET request
    print("\n1. Testing GET request to GraphQL endpoint:")
    try:
        response = requests.get(url)
        print(f"   GET Status: {response.status_code}")
        print(f"   GET Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ GET failed: {e}")
    
    # Test 2: Simple POST with query
    print("\n2. Testing POST with query string:")
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        'query': 'query { __typename }'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"   POST Status: {response.status_code}")
        print(f"   POST Headers: {dict(response.headers)}")
        print(f"   POST Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ JSON Parsed: {data}")
        else:
            print(f"   ❌ Non-200 status")
            
    except json.JSONDecodeError as e:
        print(f"   ❌ JSON decode error: {e}")
        print(f"   Raw response: {response.text}")
    except Exception as e:
        print(f"   ❌ POST failed: {e}")
    
    # Test 3: Check if CSRF is required
    print("\n3. Testing with different content types:")
    
    # Try form-encoded
    headers_form = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload_form = 'query={__typename}'
    
    try:
        response = requests.post(url, data=payload_form, headers=headers_form)
        print(f"   Form-encoded Status: {response.status_code}")
        print(f"   Form-encoded Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Form-encoded failed: {e}")
    
    # Test 4: Try with CSRF token if needed
    print("\n4. Testing Django CSRF requirements:")
    
    # First get a CSRF token
    try:
        csrf_response = requests.get(url)
        csrf_token = csrf_response.cookies.get('csrftoken')
        if csrf_token:
            print(f"   Got CSRF token: {csrf_token[:20]}...")
            
            headers_csrf = {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,
            }
            response = requests.post(url, json=payload, headers=headers_csrf, 
                                    cookies=csrf_response.cookies)
            print(f"   With CSRF Status: {response.status_code}")
            print(f"   With CSRF Response: {response.text}")
        else:
            print("   No CSRF token found in cookies")
    except Exception as e:
        print(f"   ❌ CSRF test failed: {e}")

if __name__ == "__main__":
    test_graphql_endpoint()