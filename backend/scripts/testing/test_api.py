# scripts/testing/test_api.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health/")
    print(f"Health check: {response.status_code} - {response.text}")
    return response.status_code == 200

def test_graphql_query():
    """Test GraphQL query"""
    query = {
        "query": """
        {
          emergencies {
            id
            code
            emergencyType
            status
          }
        }
        """
    }
    
    response = requests.post(
        f"{BASE_URL}/graphql/",
        json=query,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"GraphQL Query Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Emergencies found: {len(data.get('data', {}).get('emergencies', []))}")
        return True
    return False

def test_create_emergency():
    """Test creating an emergency"""
    mutation = {
        "query": """
        mutation CreateEmergency($input: EmergencyInput!) {
          createEmergency(input: $input) {
            emergency {
              id
              code
              emergencyType
              status
            }
          }
        }
        """,
        "variables": {
            "input": {
                "emergencyType": "MEDICAL",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "description": "Test emergency from API"
            }
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/graphql/",
        json=mutation,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Create Emergency Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Created emergency: {data}")
        return True
    return False

if __name__ == "__main__":
    print("🚀 Testing AlertO24 Backend API")
    print("=" * 40)
    
    tests = [
        ("Health Check", test_health),
        ("GraphQL Query", test_graphql_query),
        ("Create Emergency", test_create_emergency),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n📋 {name}:")
        try:
            success = test_func()
            results.append((name, success))
            print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results.append((name, False))
    
    print(f"\n📊 Summary: {sum(r[1] for r in results)}/{len(results)} tests passed")