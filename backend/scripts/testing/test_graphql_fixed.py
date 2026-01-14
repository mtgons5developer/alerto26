# scripts/testing/test_graphql_fixed.py

import requests


def test_graphql_endpoint():
    """Test GraphQL with proper endpoint"""
    print("🔍 Testing GraphQL endpoint...")

    # Test with trailing slash (should work)
    print("\n1. Testing with trailing slash (/graphql/):")
    response = requests.post(
        "http://localhost:8000/graphql/",
        json={"query": "{ __typename }"},
        headers={"Content-Type": "application/json"},
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:100]}...")

    # Test without trailing slash (might fail if APPEND_SLASH=True)
    print("\n2. Testing without trailing slash (/graphql):")
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ __typename }"},
            headers={"Content-Type": "application/json"},
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"   Error: {e}")

    # Test actual queries
    print("\n3. Testing emergency queries:")
    queries = [
        {"query": "{ emergencies { id emergencyType status } }"},
        {"query": "{ providers { id status serviceTypes } }"},
        {
            "query": 'mutation { createEmergency(emergencyType: "TEST", latitude: 40.7128, longitude: -74.0060) { emergency { id code } } }'
        },
    ]

    for i, query in enumerate(queries, 1):
        try:
            response = requests.post(
                "http://localhost:8000/graphql/",
                json=query,
                headers={"Content-Type": "application/json"},
            )
            print(f"   Query {i}: {response.status_code} - {len(response.text)} chars")
        except Exception as e:
            print(f"   Query {i} failed: {e}")


if __name__ == "__main__":
    test_graphql_endpoint()
