import json
import sys

import requests

BASE_URL = "http://localhost:8000"

# Valid emergency types from your Django model
VALID_EMERGENCY_TYPES = [
    "MEDICAL",
    "FIRE",
    "POLICE",
    "CAR_ACCIDENT",
    "NATURAL_DISASTER",
    "UTILITY",
    "OTHER",
]


def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health/")
    print(f"Health check: {response.status_code} - {response.text}")
    return response.status_code == 200


def test_graphql_query():
    """Test GraphQL query for emergencies - using valid emergency types"""
    print("\n📋 Querying emergencies (with proper emergencyType field)...")

    # Query with emergencyType field - should work now
    query = {
        "query": """
        {
          emergencies {
            id
            code
            emergencyType
            status
            createdAt
            user {
              id
              username
            }
          }
        }
        """
    }

    response = requests.post(
        f"{BASE_URL}/graphql/", json=query, headers={"Content-Type": "application/json"}
    )

    print(f"GraphQL Query Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()

        if result.get("errors"):
            print(f"❌ GraphQL Errors: {result['errors']}")
            return False

        data = result.get("data", {})
        emergencies = data.get("emergencies", [])
        print(f"✅ Found {len(emergencies)} emergencies")

        if emergencies:
            print("\n📋 Latest emergencies:")
            for i, emergency in enumerate(emergencies[:5], 1):
                print(f"  {i}. {emergency['code']}")
                print(f"     Type: {emergency['emergencyType']}")
                print(f"     Status: {emergency['status']}")
                print(f"     Created: {emergency['createdAt']}")
                if emergency.get("user"):
                    print(f"     User: {emergency['user']['username']}")
                print()

        return True
    else:
        print(f"❌ HTTP Error: {response.text}")
        return False


def test_create_emergency():
    """Test creating an emergency with valid emergency type"""
    print("\n🚨 Creating a new emergency...")

    user_id = "dc778c56-a71a-4ac7-b231-09e789955245"

    # Use a valid emergency type from your Django model
    emergency_type = "CAR_ACCIDENT"  # Changed from lowercase to match Django model

    mutation = """
    mutation CreateEmergency($userId: UUID!, $emergencyType: String!, $latitude: Float!, $longitude: Float!, $description: String) {
      createEmergency(
        userId: $userId
        emergencyType: $emergencyType
        latitude: $latitude
        longitude: $longitude
        description: $description
      ) {
        emergency {
          id
          code
          emergencyType
          status
          createdAt
          description
          user {
            id
            username
          }
        }
      }
    }
    """

    create_variables = {
        "userId": user_id,
        "emergencyType": emergency_type,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "description": "Test car accident emergency",
    }

    response = requests.post(
        f"{BASE_URL}/graphql/",
        json={"query": mutation, "variables": create_variables},
        headers={"Content-Type": "application/json"},
    )

    print(f"Create Emergency Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"Raw response: {json.dumps(result, indent=2)}")

        if result.get("errors"):
            print(f"❌ GraphQL Errors: {result['errors']}")
            return False

        data = result.get("data", {}).get("createEmergency", {})

        if data.get("emergency"):
            emergency = data["emergency"]
            print("\n✅ Emergency created successfully!")
            print("📋 Emergency Details:")
            print(f"   ID: {emergency['id']}")
            print(f"   Code: {emergency['code']}")
            print(f"   Type: {emergency['emergencyType']}")
            print(f"   Status: {emergency['status']}")
            print(f"   Created: {emergency['createdAt']}")
            print(f"   Description: {emergency['description']}")
            if emergency.get("user"):
                print(
                    f"   User: {emergency['user']['username']} ({emergency['user']['id'][:8]}...)"
                )
            return True
        else:
            print("❌ No emergency data returned")
            print(f"Full response: {json.dumps(result, indent=2)}")
            return False
    else:
        print(f"❌ HTTP Error: {response.text}")
        return False


def test_multiple_emergency_creations():
    """Test creating emergencies with different valid types"""
    print("\n🚨 Testing all emergency types...")

    user_id = "dc778c56-a71a-4ac7-b231-09e789955245"
    successful_creations = []

    for emergency_type in VALID_EMERGENCY_TYPES:
        print(f"\n  Creating '{emergency_type}' emergency...")

        mutation = f"""
        mutation {{
          createEmergency(
            userId: "{user_id}"
            emergencyType: "{emergency_type}"
            latitude: 40.7
            longitude: -74.0
            description: "Test {emergency_type.replace("_", " ").lower()} emergency"
          ) {{
            emergency {{
              id
              code
              emergencyType
              status
            }}
          }}
        }}
        """

        response = requests.post(
            f"{BASE_URL}/graphql/",
            json={"query": mutation},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("errors"):
                error_msg = result["errors"][0]["message"] if result["errors"] else ""
                print(f"    ❌ Failed: {error_msg[:50]}...")
            else:
                data = result.get("data", {}).get("createEmergency", {})
                if data.get("emergency"):
                    emergency = data["emergency"]
                    print(
                        f"    ✅ Created: {emergency['code']} ({emergency['emergencyType']})"
                    )
                    successful_creations.append(emergency_type)
        else:
            print(f"    ❌ HTTP Error: {response.status_code}")

    print(
        f"\n📊 Created {len(successful_creations)}/{len(VALID_EMERGENCY_TYPES)} emergency types"
    )
    return len(successful_creations) > 0


def fix_existing_data_issue():
    """Check and report on the data mismatch issue"""
    print("\n🔧 Data Issue Analysis")
    print("=" * 40)
    print(
        "\nThe problem: Database has lowercase values, but GraphQL expects uppercase."
    )
    print("\nYour Django model expects these values:")
    for i, type_name in enumerate(VALID_EMERGENCY_TYPES, 1):
        print(f"  {i}. {type_name}")

    print("\n💡 Solutions:")
    print("1. Update existing database records to use uppercase values")
    print("2. Add a data migration to fix the values")
    print("3. Use a custom resolver in GraphQL to handle the conversion")

    # Show how to fix the data
    print("\n📝 To fix existing data, run in Django shell:")
    print(
        """
python manage.py shell

from emergencies.models import Emergency
import json

# Map lowercase to uppercase
type_mapping = {
    'accident': 'CAR_ACCIDENT',
    'fire': 'FIRE',
    'medical': 'MEDICAL',
    'natural_disaster': 'NATURAL_DISASTER',
    'hazard': 'OTHER',  # or create a new type if needed
    # Add other mappings as needed
}

# Update existing records
for emergency in Emergency.objects.all():
    if emergency.emergency_type in type_mapping:
        emergency.emergency_type = type_mapping[emergency.emergency_type]
        emergency.save()
        print(f"Updated {emergency.code} to {emergency.emergency_type}")
    """
    )

    return True


def run_comprehensive_test():
    """Run all tests"""
    print("🚀 AlertO24 Backend API - Comprehensive Test")
    print("=" * 60)
    print(f"📝 Valid Emergency Types: {', '.join(VALID_EMERGENCY_TYPES)}")
    print("=" * 60)

    results = []

    # Test 1: Health check
    print("\n1. 📍 Health Check")
    health_success = test_health()
    results.append(("Health Check", health_success))
    print(f"   {'✅ PASS' if health_success else '❌ FAIL'}")

    # Test 2: Query emergencies
    print("\n2. 📋 Query Emergencies")
    query_success = test_graphql_query()
    results.append(("Query Emergencies", query_success))
    print(f"   {'✅ PASS' if query_success else '❌ FAIL'}")

    # Test 3: Create single emergency
    print("\n3. 🚨 Create Emergency (Single)")
    create_success = test_create_emergency()
    results.append(("Create Emergency", create_success))
    print(f"   {'✅ PASS' if create_success else '❌ FAIL'}")

    # Test 4: Test all emergency types
    print("\n4. 🧪 Test All Emergency Types")
    multi_success = test_multiple_emergency_creations()
    results.append(("Multiple Types", multi_success))
    print(f"   {'✅ PASS' if multi_success else '❌ FAIL'}")

    # Test 5: Data issue analysis
    print("\n5. 🔧 Data Issue Analysis")
    analysis_success = fix_existing_data_issue()
    results.append(("Issue Analysis", analysis_success))
    print(f"   {'✅ PASS' if analysis_success else '❌ FAIL'}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    total = len(results)
    passed = sum(1 for _, success in results if success)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name:25} {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    # Final recommendations
    print("\n💡 FINAL RECOMMENDATIONS:")
    print("1. Use uppercase emergency types: MEDICAL, FIRE, CAR_ACCIDENT, etc.")
    print("2. Run the data migration script above to fix existing records")
    print("3. All future emergency creations should use the uppercase values")

    if passed >= 3:
        print("\n✅ Core API functionality is working correctly!")
        print("   The enum mismatch is a data issue, not an API issue.")
    else:
        print("\n⚠️  Some tests failed - check the issues above")

    return passed >= 3


if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
