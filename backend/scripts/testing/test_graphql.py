# test_graphql.py

import requests

url = "http://localhost:8000/graphql/"

# Test query
query = """
{
  emergencies {
    code
    emergencyType
    priority
    status
    city
    isAnonymous
  }
  providers {
    status
    serviceTypes
    rating
  }
}
"""

try:
    response = requests.post(url, json={"query": query})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        emergencies = data.get("data", {}).get("emergencies", [])
        providers = data.get("data", {}).get("providers", [])

        print(
            f"\n✅ Found {len(emergencies)} emergencies and {len(providers)} providers"
        )
        print("\n📊 Sample data:")
        if emergencies:
            print(f"First emergency: {emergencies[0]}")
        if providers:
            print(f"First provider: {providers[0]}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Connection error: {e}")
